### Gaussian Splats 3D: Internal Documentation

#### 1) Splat primitive data representation
- **Uncompressed CPU layout** (`UncompressedSplatArray` at lines 4–59): each splat is a 14-element array in this order:
  - `x, y, z` (center), `scale_0, scale_1, scale_2` (axis-aligned log-scales -> later exponentiated where relevant),
  - quaternion `rot_0..rot_3` (x, y, z, w),
  - `f_dc_0, f_dc_1, f_dc_2` (DC color or RGB), `opacity` (0–255).
  - Offsets are defined in `UncompressedSplatArray.OFFSET`.
```1:59:web/gaussian-splats-3d.module.js
class UncompressedSplatArray {

    static OFFSET = {
        X: 0,
        Y: 1,
        Z: 2,
        SCALE0: 3,
        SCALE1: 4,
        SCALE2: 5,
        ROTATION0: 6,
        ROTATION1: 7,
        ROTATION2: 8,
        ROTATION3: 9,
        FDC0: 10,
        FDC1: 11,
        FDC2: 12,
        OPACITY: 13
    };
...
```
- **Packed/streamed layout** (`SplatBuffer`, lines 287+): two compression levels are supported.
  - Level 0 (float): 44 bytes/splat → centers(3xfloat32), scales(3xfloat32), rotation(4xfloat32), color(4xuint8).
  - Level 1 (quantized/half-floats): centers/scales/rot quantized (uint16/half), colors uint8; bucket-based delta for centers; 24 bytes/splat. See `SplatBuffer.CompressionLevels`.
```287:319:web/gaussian-splats-3d.module.js
class SplatBuffer {
...
    static CompressionLevels = {
        0: { BytesPerCenter: 12, BytesPerColor: 4, BytesPerScale: 12, BytesPerRotation: 16, BytesPerSplat: 44, ScaleRange: 1 },
        1: { BytesPerCenter: 6,  BytesPerColor: 4, BytesPerScale: 6,  BytesPerRotation: 8,  BytesPerSplat: 24, ScaleRange: 32767 }
    };
```
- **Covariance on CPU**: per-splat 3D covariance is computed from `scale` and `rotation`, optionally transformed by a 4x4 world matrix. Stored as 6 floats representing the symmetric 3x3: `[m00, m01, m02, m11, m12, m22]`.
```480:523:web/gaussian-splats-3d.module.js
static computeCovariance = function() {
...
    transformedCovariance.copy(covarianceMatrix).transpose().premultiply(covarianceMatrix);
    if (transform) { /* apply world 3x3 */ }
    if (desiredOutputCompressionLevel === 1) { /* write half */ } else { /* write float */ }
};
```

#### 2) PLY processing pipeline
- **Uncompressed PLY** (`PlyParser`, lines 1526+):
  - Header is parsed to find property names/types and bytes-per-vertex; `Fields` include `scale_0..2`, `rot_0..3`, `x,y,z`, `f_dc_*` or `red,green,blue`, `opacity`.
  - Each vertex row is decoded into an uncompressed splat via `parseToUncompressedSplat` and then written to an output `ArrayBuffer` section in `parseToUncompressedSplatBufferSection`.
```1526:1681:web/gaussian-splats-3d.module.js
class PlyParser {
    static Fields = ['scale_0','scale_1','scale_2','rot_0','rot_1','rot_2','rot_3','x','y','z','f_dc_0','f_dc_1','f_dc_2','red','green','blue','opacity'];
...
    static parseToUncompressedSplatBufferSection(header, fromSplat, toSplat, vertexData, vertexDataOffset, toBuffer, toOffset) {
        const outBytesPerCenter = SplatBuffer.CompressionLevels[0].BytesPerCenter; /* writes center/scale/rot/color */
    }
}
```
- **Compressed PLY** (`CompressedPlyParser`, lines 1168+):
  - Header describes chunk-level position/scale extremes and per-vertex packed fields (`packed_position`, `packed_rotation`, `packed_scale`, `packed_color`).
  - Decompression expands each vertex into `UncompressedSplatArray` via `decompressSplat`, using custom packings `unpack111011`, `unpackRot`, `unpack8888` and per-chunk extremes with `lerp`.
  - The decompressed data is written to a contiguous uncompressed section buffer in `parseToUncompressedSplatBufferSection`.
```1412:1451:web/gaussian-splats-3d.module.js
static decompressSplat = function() {
  /* unpack packed position/rotation/scale/color, apply extremes, exp for scales, clamp colors */
  return outSplat;
}();
```
- **Streaming loader** (`PlyLoader.loadFromURL`, lines 1953+): progressively downloads, detects header (compressed/uncompressed), pre-sizes a unified `SplatBuffer`, and incrementally fills sections using the appropriate parser.
```1953:2010:web/gaussian-splats-3d.module.js
class PlyLoader {
  static loadFromURL(fileName, onProgress, streamLoadData, onStreamedSectionProgress, minimumAlpha, compressionLevel, sectionSize, sceneCenter, blockSize, bucketSize) {
    /* detect header, choose CompressedPlyParser or PlyParser, stream-fill output buffer */
  }
}
```

#### 3) GPU representation of splat data
- **Data textures** (`SplatMesh.uploadSplatDataToTextures`, lines 6755+): CPU arrays are packed into textures for rendering:
  - `covariancesTexture` (RG format): 3 texels per splat, storing the 6 unique elements of the symmetric 3x3 covariance in float32 or half-float.
  - `centersColorsTexture` (RGBA32UI): 1 texel per splat with 4 uint32 channels: [packed RGBA color, float32 x, float32 y, float32 z] where floats are bit-cast to uint using `uintEncodedFloat`.
  - If dynamic: `transformIndexesTexture` (R32UI): 1 texel per splat mapping to scene transform index.
```6786:6869:web/gaussian-splats-3d.module.js
const covTex = new THREE.DataTexture(paddedCovariances, w, h, THREE.RGFormat, covariancesTextureType);
const centersColsTex = new THREE.DataTexture(paddedCentersCols, w, h, THREE.RGBAIntegerFormat, THREE.UnsignedIntType);
centersColsTex.internalFormat = 'RGBA32UI';
/* dynamic */ transformIndexesTexture.internalFormat = 'R32UI';
```
- **Geometry**: an instanced quad per splat with an attribute `splatIndex` used to fetch that splat’s data from the textures; base quad vertices at [-1, -1]..[1, 1].
```6448:6460:web/gaussian-splats-3d.module.js
static buildGeomtery(maxSplatCount) {
  /* index + 4-vertex quad, instanced with attribute 'splatIndex' */
}
```

#### 4) Rendering and shaders
- **Material and shaders** (`SplatMesh.buildMaterial`, lines 6107+): creates a `THREE.ShaderMaterial` with custom vertex/fragment shaders.
  - Vertex shader responsibilities:
    - Fetch per-splat packed data via `splatIndex` from `centersColorsTexture` and `covariancesTexture`.
    - If dynamic, fetch transform index and apply scene transform.
    - Project center; build Jacobian for perspective; transform 3D covariance to 2D covariance in screen space.
    - Eigen-decompose 2x2 covariance to get ellipse axes; scale quad basis to sqrt(8) sigma; set `vPosition`, `vColor`.
  - Fragment shader:
    - Compute `A = dot(vPosition, vPosition)`; discard if outside ellipse (A > 8).
    - Evaluate gaussian opacity `exp(-0.5 * A) * vColor.a`; output `vec4(color, opacity)`.
```6107:6343:web/gaussian-splats-3d.module.js
static buildMaterial(...) { /* builds vertexShaderSource + fragmentShaderSource shown in-code */ }
```
- **Render loop** (`Viewer.render`, lines 9637+): draws Three scene, then `SplatMesh` with its shader, plus overlays.
```9648:9654:web/gaussian-splats-3d.module.js
this.renderer.autoClear = false;
if (hasRenderables(this.threeScene)) this.renderer.render(this.threeScene, this.camera);
this.renderer.render(this.splatMesh, this.camera);
```
- **GPU sort/distance precomputation (optional)**: WebGL2 transform feedback program to compute per-splat depths for sorting; small custom shaders built in `setupDistancesComputationTransformFeedback` (7116+).

#### 5) Gaussian kernel and spherical harmonics
- **Gaussian kernel evaluation**: done entirely in the shaders.
  - The vertex shader projects 3D covariance to screen-space 2D covariance, derives ellipse basis via eigen-decomposition, and scales the quad to cover √8σ.
  - The fragment shader evaluates the radial gaussian: `opacity = exp(-0.5 * A) * alpha` where `A = dot(vPosition, vPosition)` after the vertex-space scaling that makes the inverse covariance the identity.
```6327:6343:web/gaussian-splats-3d.module.js
float A = dot(vPosition, vPosition);
if (A > 8.0) discard;
float opacity = exp(-0.5 * A) * vColor.a;
```
- **Spherical harmonics (SH)**: Only the DC component is used when present.
  - During PLY parsing, if `f_dc_0..2` exist, they are converted to RGB via `0.5 + C0 * f_dc_i` with `C0 = 0.28209479177387814` then scaled to 0–255 and clamped. Otherwise RGB fields are used. Opacity is passed through a sigmoid and scaled to 0–255.
  - Higher-order SH are not evaluated; TODOs note future support. No SH evaluation is present in shaders.
```1703:1719:web/gaussian-splats-3d.module.js
const SH_C0 = 0.28209479177387814; /* DC */
newSplat[OFFSET.FDCi] = (0.5 + SH_C0 * rawVertex['f_dc_i']) * 255;
/* opacity sigmoid */
```

#### Notes on indexing and transforms
- `SplatBuffer.getSplatCenter/Scale/Rotation/Color` decode either float or quantized representations per section, with bucket-level offsets for centers in compression level 1 (lines 373–420).
- The CPU-prepared 3D covariance is what the vertex shader samples to derive screen-space ellipses; no full 2D conic is stored, just the symmetric 3x3 covariance compacted to 6 values.
- For dynamic multi-scene, per-splat `transformIndex` selects one of `transforms[MaxScenes]` set as a uniform array.

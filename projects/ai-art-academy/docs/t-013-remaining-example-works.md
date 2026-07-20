# t-013 — Remaining Academy example works handoff

Date: 2026-07-17
Target repository: `silasfelinus/kind_robots`
Intended branch: `worker/ai-art-academy-t-013`

**Correction (2026-07-20, t-010 roadmap-accuracy cycle):** the "Files to
change" list below is stale about *where* 4 of the 5 files live. Confirmed
via `kind_robots` source (`utils/scripts/mediaContractSource.ts`,
`verifyAcademyExamplesManifest.ts`) and a live check
(`get_file_contents(silasfelinus/kind_robots,
public/images/academy/examples)` 404s — the directory does not exist in
git): `examples.manifest.json` and every example-work image are read from
`https://media.acrocatranch.com/images/academy/examples/...` at build/test
time (or a local `MEDIA_ROOT` mirror), NOT from the kind_robots git tree.
Only `stores/seeds/academyStyles.ts` is an actual git commit in this repo.
The `"file": "public/images/..."` strings inside each manifest entry below
are correct as-is — that's the schema's identifier convention
(`repositoryFileToMediaPath` strips the `public/images/` prefix to resolve
the real media-server path) — just don't try to `git add`/commit those 4
paths into `kind_robots`. This is the same media-server-write blocker
already tracked on ai-art-academy/t-033 and t-035: applying the manifest
and image uploads requires home-relay access
(`ops/home-server/SELF-HOSTED-MEDIA.md`), which no sandboxed agent session
has. A session with that access should upload the 3 images and the merged
manifest JSON through the relay, THEN a normal sandboxed session can land
the `academyStyles.ts` half as an ordinary PR.

## Why this handoff exists

The source research and file acquisition are complete, but the current GitHub connector can only replace an existing file as a complete blob. The canonical registry is `stores/seeds/academyStyles.ts` (about 1,100 lines), so replacing it through a truncated connector response would risk dropping unrelated curriculum content. Per the cross-repo fallback rule, this document preserves the exact scoped patch for a local-checkout session.

No backend, schema, deployment, secret, or billing change is required.

## Files to change

In the `kind_robots` git repo (normal PR):

- `stores/seeds/academyStyles.ts`

On the media server (`media.acrocatranch.com`), via the home relay —
**not** a kind_robots git commit (see correction note above):

- `academy/examples/examples.manifest.json` (merge these 3 entries into the existing array)
- `academy/examples/the-yellow-cow-49-1210.jpg` (new)
- `academy/examples/fantomas-1976-59-1.jpg` (new)
- `academy/examples/composition-8-37-262.jpg` (new)

## 1. Expressionism

Verified work:

- Work: **The Yellow Cow**
- Artist: Franz Marc (died 1916)
- Year: 1911
- Collection: Solomon R. Guggenheim Museum
- Accession: `49.1210`
- Source page: `https://commons.wikimedia.org/wiki/File:Franz_Marc-The_Yellow_Cow-1911.jpg`
- Original image: `https://upload.wikimedia.org/wikipedia/commons/f/fd/Franz_Marc-The_Yellow_Cow-1911.jpg`
- License: `PD-Mark`
- License terms: `https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia`
- Verified public-domain basis: artist died in 1916; work published before 1931; Commons identifies the faithful reproduction as public domain.
- Acquired file: 1067×797 JPEG, 101,693 bytes.

Add before the `remix` field of the `expressionism` entry:

```ts
    exampleWorks: [
      {
        workTitle: 'The Yellow Cow',
        artist: 'Franz Marc',
        artistDied: 1916,
        year: '1911',
        collection: 'Solomon R. Guggenheim Museum',
        accessionId: '49.1210',
        sourceUrl:
          'https://commons.wikimedia.org/wiki/File:Franz_Marc-The_Yellow_Cow-1911.jpg',
        license: 'PD-Mark',
        licenseTermsUrl:
          'https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia',
        imageSrc: '/images/academy/examples/the-yellow-cow-49-1210.jpg',
      },
    ],
```

Manifest entry:

```json
{
  "movement": "expressionism",
  "file": "public/images/academy/examples/the-yellow-cow-49-1210.jpg",
  "workTitle": "The Yellow Cow",
  "artist": "Franz Marc",
  "artistDied": 1916,
  "year": "1911",
  "collection": "Solomon R. Guggenheim Museum",
  "accessionId": "49.1210",
  "sourceUrl": "https://commons.wikimedia.org/wiki/File:Franz_Marc-The_Yellow_Cow-1911.jpg",
  "license": "PD-Mark",
  "licenseTermsUrl": "https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia",
  "retrievedDate": "2026-07-17",
  "width": 1067,
  "height": 797,
  "bytes": 101693
}
```

## 2. Cubism

Verified work:

- Work: **Fantômas**
- Artist: Juan Gris (died 1927)
- Year: 1915
- Collection: National Gallery of Art, Washington
- Accession: `1976.59.1`
- Source page: `https://www.nga.gov/artworks/56101-fantomas`
- Original NGA image: `https://api.nga.gov/iiif/dd10b4c4-bc3b-430f-8c6f-918a3ef2cb3b/full/full/0/default.jpg?attachment_filename=fantomas_1976.59.1.jpg`
- License: `CC0`
- License terms: `https://www.nga.gov/artworks/free-images-and-open-access`
- Verification: the NGA object page labels the media free and public domain and supplies the accession number.
- Acquired file: resized from the NGA original to 1600×1322 JPEG, quality 88, 680,178 bytes, matching the existing examples' long-edge convention.

Add before the `remix` field of the `cubism` entry:

```ts
    exampleWorks: [
      {
        workTitle: 'Fantômas',
        artist: 'Juan Gris',
        artistDied: 1927,
        year: '1915',
        collection: 'National Gallery of Art, Washington',
        accessionId: '1976.59.1',
        sourceUrl: 'https://www.nga.gov/artworks/56101-fantomas',
        license: 'CC0',
        licenseTermsUrl:
          'https://www.nga.gov/artworks/free-images-and-open-access',
        imageSrc: '/images/academy/examples/fantomas-1976-59-1.jpg',
      },
    ],
```

Manifest entry:

```json
{
  "movement": "cubism",
  "file": "public/images/academy/examples/fantomas-1976-59-1.jpg",
  "workTitle": "Fantômas",
  "artist": "Juan Gris",
  "artistDied": 1927,
  "year": "1915",
  "collection": "National Gallery of Art, Washington",
  "accessionId": "1976.59.1",
  "sourceUrl": "https://www.nga.gov/artworks/56101-fantomas",
  "license": "CC0",
  "licenseTermsUrl": "https://www.nga.gov/artworks/free-images-and-open-access",
  "retrievedDate": "2026-07-17",
  "width": 1600,
  "height": 1322,
  "bytes": 680178
}
```

## 3. Bauhaus

Verified work:

- Work: **Composition 8 (Komposition 8)**
- Artist: Wassily Kandinsky (died 1944)
- Year: July 1923
- Collection: Solomon R. Guggenheim Museum
- Accession: `37.262`
- Source page: `https://commons.wikimedia.org/wiki/File:Kandinsky_-_Composition_8,_1923.jpg`
- Original image: `https://upload.wikimedia.org/wikipedia/commons/0/02/Kandinsky_-_Composition_8%2C_1923.jpg`
- License: `PD-Mark`
- License terms: `https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia`
- Verification: Commons marks the faithful reproduction public domain; the Guggenheim record identifies the work as a 1923 Bauhaus-period Kandinsky and gives accession `37.262`.
- Acquired file: 980×682 JPEG, 218,875 bytes.

Add before the `remix` field of the `bauhaus` entry:

```ts
    exampleWorks: [
      {
        workTitle: 'Composition 8 (Komposition 8)',
        artist: 'Wassily Kandinsky',
        artistDied: 1944,
        year: 'July 1923',
        collection: 'Solomon R. Guggenheim Museum',
        accessionId: '37.262',
        sourceUrl:
          'https://commons.wikimedia.org/wiki/File:Kandinsky_-_Composition_8,_1923.jpg',
        license: 'PD-Mark',
        licenseTermsUrl:
          'https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia',
        imageSrc: '/images/academy/examples/composition-8-37-262.jpg',
      },
    ],
```

Manifest entry:

```json
{
  "movement": "bauhaus",
  "file": "public/images/academy/examples/composition-8-37-262.jpg",
  "workTitle": "Composition 8 (Komposition 8)",
  "artist": "Wassily Kandinsky",
  "artistDied": 1944,
  "year": "July 1923",
  "collection": "Solomon R. Guggenheim Museum",
  "accessionId": "37.262",
  "sourceUrl": "https://commons.wikimedia.org/wiki/File:Kandinsky_-_Composition_8,_1923.jpg",
  "license": "PD-Mark",
  "licenseTermsUrl": "https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia",
  "retrievedDate": "2026-07-17",
  "width": 980,
  "height": 682,
  "bytes": 218875
}
```

## Verification required after applying

Run from the `kind_robots` checkout:

```bash
npm run test:academy-examples-manifest
npm run prettier:check
npm run typecheck
```

Also verify:

1. `examples.manifest.json` remains valid JSON and contains exactly one record per movement.
2. Each `imageSrc` maps to the corresponding `public/` file.
3. `academyStyles.ts` and the manifest use identical movement/file pairs.
4. The Academy lesson detail shows all 21 movements with an example work.

## Remaining action

Two independent steps, per the correction note above:

1. **Media upload (needs home-relay access):** merge the three manifest entries into `examples.manifest.json` and upload the three acquired JPEGs on `media.acrocatranch.com` under `academy/examples/`.
2. **Git PR (any sandboxed session):** apply the three `exampleWorks` patches to `stores/seeds/academyStyles.ts` in `kind_robots`, open the normal scoped PR, and merge after the contract verifier and TypeScript checks pass.

Do not mark the live implementation complete merely because this handoff is merged into Conductor — both steps must land, and `npm run test:academy-examples-manifest` (ideally with `MEDIA_VERIFY_ASSETS=1`) must pass against the real media server.

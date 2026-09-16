# Direct self-hosted media delivery

Kind Robots image URLs remain `/images/...`, but generated Kind Robots assets
are written directly to the self-hosted media share rather than committed to the
Kind Robots Git repository.

## Verified infrastructure

- Public origin: `https://media.acrocatranch.com/images/...`
- Unraid path: `/mnt/user/pc/kindrobots/images`
- Windows path: `Z:\kindrobots\images`
- WSL path: `/mnt/z/kindrobots/images`
- Nginx container: `media`

The Windows home relay uses the Windows path because ComfyUI, Python,
and pm2 run in Windows rather than WSL.

## How direct delivery works

1. The media-aware consumers attach the existing logical destination to the
   ArtJob payload as `targetRepo` and `imagePath`.
2. `relay_media_agent.py` renders with the existing `relay_agent.py` functions.
3. For a Kind Robots target under `public/images/`, the relay writes the exact
   equivalent path under `KR_MEDIA_IMAGES_DIR`.
4. The relay atomically refreshes the folder's `gallery.json` and the root
   `collections.json`.
5. Only after those writes succeed does it mark the ArtJob complete.
6. The GitHub consumer performs a public HEAD request against the media origin.
   If verification fails, it keeps a recoverable copy in `projects/process/`.

Conductor-owned generated project images continue to use the existing
`projects/process/` and `projects/images/` flow. Large binary media that is not
usefully versioned as source text, such as project video masters, may instead live
on the self-hosted media origin when the project records a stable public media URL.
This is a storage policy, not permission to delete a tracked source file.

## Conductor large-binary migration policy

For a tracked Conductor binary being moved to self-hosted media:

1. Treat the tracked file as the only copy until proven otherwise.
2. Upload or copy it to the intended media path using a machine with the media share mounted.
3. Perform a public `HEAD` request against the exact final media URL and require HTTP 200.
4. Update every project document or data record that refers to the tracked path so it points at the verified media URL.
5. Only after steps 2-4 succeed may a separate, reviewable change remove the tracked binary from the current tree.
6. Do not rewrite Git history to reclaim old object bytes. The goal is to stop repository growth without invalidating existing clones.

If the media share is unavailable, the upload cannot be verified, or the public
probe is anything other than 200, leave the tracked binary in place. A local copy,
an intended URL, or a successful upload without the public probe is not delivery.

This policy does not move ordinary Conductor project images out of the existing
image-distribution pipeline. It provides an explicit home for unusually large
binary assets where Git is serving as an expensive file bucket rather than useful
version history.

## Windows relay rollout

From PowerShell on Silas-PC:

```powershell
setx KR_MEDIA_IMAGES_DIR "Z:/kindrobots/images"
py -3.12 -m pip install Pillow
```

Open a new PowerShell window after `setx`, pull the change, and restart the
Windows pm2 relay with updated environment variables:

```powershell
cd D:\code\conductor
git pull
cd ops\home-server
pm2 restart ecosystem.config.js --only kr-relay --update-env
pm2 save
pm2 logs kr-relay --lines 50
```

Expected startup line:

```text
agent <hostname> polling https://kind-robots.vercel.app every 10.0s
```

For a direct job, expect:

```text
job <id>: COMFY direct media -> <relative path>
direct media: Z:\kindrobots\images\<relative path>
job <id>: DONE (...; media ...)
```

## Smoke test

Before enabling the revised GitHub workflows, run one pending Kind Robots art
request from the Conductor checkout:

```powershell
$env:KR_MEDIA_ORIGIN = "https://media.acrocatranch.com"
python scripts\consume_art_requests_to_media.py --live --limit 1 --timeout 900
```

Then verify the path reported by the relay exists both locally and publicly:

```powershell
Get-Item "Z:\kindrobots\images\<relative-path>"
curl.exe -I "https://media.acrocatranch.com/images/<relative-path>"
```

The consumer should say that the home relay wrote directly to self-hosted media.
No matching binary should appear in `kind_robots/public/images` or remain in
`conductor/projects/process`.

## Rollback

The rollout is intentionally wrapper-based:

1. Change the pm2 relay script from `relay_media_agent.py` back to
   `relay_agent.py`.
2. Change GitHub workflow commands back to `consume_art_queue.py` and
   `consume_art_requests.py`.
3. The existing projects/process distributor remains available throughout.

No database URL migration is involved. ArtImage records and front-end content
continue using `/images/...`.

## Final Kind Robots repository migration

After the direct smoke test succeeds:

1. Run the final incremental rsync from Kind Robots to Unraid without `--delete`.
2. Verify representative app pages and folder collections against the media origin.
3. Stop accepting new binaries under `kind_robots/public/images`.
4. Remove the tracked image tree in a separate PR only after the public copies are verified.
5. Leave Git history intact. Historical object size is accepted; future binary growth is the problem this policy prevents.

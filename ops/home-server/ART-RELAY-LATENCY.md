# Art relay latency

`kr-relay` polls the Kind Robots ArtJob queue every two seconds by default through the PM2 `POLL_SECONDS` environment value.

After pulling this change on the render host, reload the PM2 environment:

```powershell
pm2 restart kr-relay --update-env
pm2 save
```

The relay remains pull-only: Kind Robots never opens a connection into the home network. Override `POLL_SECONDS` only when intentionally trading responsiveness for fewer idle claim requests.

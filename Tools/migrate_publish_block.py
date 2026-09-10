#!/usr/bin/env python3
"""One-off: rewrite every story.yaml's flat publish block into the two-environment
shape introduced with the staging/production split. See Docs/06-decisions.md D28.

The old block recorded two booleans and no timestamps, so the real upload times
are simply not recoverable. Rather than invent them, this backfills
production.uploadedAt/rowUpsertedAt from card.publishedAt — an editorial date
standing in for an unrecorded event — and marks every story it touches with
legacyDirectToProduction: true. staging.* is left empty, because it is true that
none of these stories ever passed through a staging environment.

bucketID and objectPath are read from the live production catalog, not derived,
so what lands in the manifest is what is actually there.

Safe to run twice: a manifest already in the new shape is left alone.
"""
import argparse, io, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lullable as L

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--assets", default="/tmp/prod_assets.json",
                    help="story_id -> {aid,bucket_id,object_path} exported from production")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    prod = json.load(io.open(a.assets, encoding="utf-8")) if os.path.exists(a.assets) else {}
    if not prod:
        print("no production asset export at %s — refusing to guess object paths" % a.assets)
        sys.exit(1)

    changed = skipped = 0
    for d in L.story_dirs(a.root):
        m = L.load_manifest(d)
        pub = m.get("publish") or {}
        sid = m.get("storyID")
        if "staging" in pub and "production" in pub:
            skipped += 1; continue

        aid = pub.get("audioAssetID", "PENDING")
        landed = bool(pub.get("supabaseAudioUploaded")) and bool(pub.get("catalogRowUpserted"))
        when = L._get(m, "card.publishedAt") or ""
        if L.parse_iso_utc(when) is None: when = ""

        live = prod.get(sid) or {}
        bucket = live.get("bucket_id") or "PENDING"
        path = live.get("object_path") or "PENDING"
        if live and live.get("aid") != aid:
            print("  !! %s: manifest asset %r but production serves %r" % (sid, aid, live.get("aid")))

        new = {"audioAssetID": aid, "bucketID": bucket, "objectPath": path,
               "staging":    {"uploadedAt": "", "rowUpsertedAt": "", "verifiedAt": ""},
               "production": {"uploadedAt": when if landed else "",
                              "rowUpsertedAt": when if landed else "",
                              "verifiedAt": ""}}
        if landed:
            new["legacyDirectToProduction"] = True
        m["publish"] = new
        print("  %-44s %s" % (sid, "legacy -> production %s" % when if landed else "not published"))
        if not a.dry_run:
            L.save_manifest(d, m)
        changed += 1

    print("\n%s %d manifest(s); %d already migrated" %
          ("would rewrite" if a.dry_run else "rewrote", changed, skipped))

if __name__ == "__main__":
    main()

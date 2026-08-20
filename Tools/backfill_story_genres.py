#!/usr/bin/env python3
"""One-off: give every story its genre row.

The 26 stories were published by hand-written SQL that skipped story_genres
entirely, so only 4 of them are linked to a genre and the `gentle-nature` genre
row was never created at all. Docs/06-decisions.md D28.

Stories published through `lullable.py publish` fix their own link, so this is
only needed for the backlog that predates it. Generated from card.genreIDs in
each manifest — nothing here is typed by hand.

Idempotent: every statement is ON CONFLICT DO NOTHING, and a story missing from
the target database is skipped rather than guessed at.
"""
import argparse, io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lullable as L

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--env", required=True, choices=L.ENV_NAMES)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    want = {}
    for d in L.story_dirs(a.root):
        m = L.load_manifest(d)
        want[m.get("storyID")] = [g for g in (L._get(m, "card.genreIDs") or [])]

    L.link_to(a.root, a.env)
    rows = L.sb_rows(a.root, "select id from public.stories;")
    if rows is None:
        print("could not read %s — nothing done." % a.env); sys.exit(1)
    present = {r["id"] for r in rows}

    missing_from_db = sorted(set(want) - present)
    todo = {s: g for s, g in want.items() if s in present and g}
    if missing_from_db:
        print("not in %s, skipped: %s" % (a.env, ", ".join(missing_from_db)))

    linked = L.sb_rows(a.root, "select story_id, genre_id from public.story_genres;") or []
    have = {(r["story_id"], r["genre_id"]) for r in linked}
    need = [(s, g) for s, gs in sorted(todo.items()) for g in gs if (s, g) not in have]
    genres_needed = sorted({g for _s, g in need})

    print("%d story/genre link(s) missing in %s across %d genre(s)"
          % (len(need), a.env, len(genres_needed)))
    if not need:
        print("nothing to do."); return

    out = ["-- GENERATED from card.genreIDs by Tools/backfill_story_genres.py — do not edit.",
           "-- target: %s (%s)" % (a.env, L.ENVIRONMENTS[a.env]["displayName"]), "", "begin;", ""]
    for g in genres_needed:
        n, sub, sym, hexv, order = L.GENRE_ROWS[g]
        out += ["insert into public.genres (id, name, subtitle, symbol_name, color_hex, sort_order, is_active)",
                "values (%s, %s, %s, %s, %s, %d, true) on conflict (id) do nothing;"
                % (L._sql(g), L._sql(n), L._sql(sub), L._sql(sym), L._sql(hexv), order)]
    out.append("")
    out.append("insert into public.story_genres (story_id, genre_id) values")
    out.append(",\n".join("  (%s, %s)" % (L._sql(s), L._sql(g)) for s, g in need))
    out.append("on conflict do nothing;")
    out += ["", "commit;", "",
            "select g.id, g.name, count(sg.story_id) as stories",
            "from public.genres g left join public.story_genres sg on sg.genre_id = g.id",
            "group by g.id, g.name order by g.id;"]
    sql = "\n".join(out) + "\n"

    path = os.path.join(a.root, "_generated-backfill-genres-%s.sql" % a.env)
    io.open(path, "w", encoding="utf-8").write(sql)
    if a.dry_run:
        print("\n" + sql); print("dry run — %s written, nothing executed." % path); return

    code, res = L.sb(a.root, ["db", "query", "--linked", "--file", os.path.basename(path)])
    if code != 0:
        print("backfill failed — nothing committed (the whole thing is one transaction).")
        sys.exit(1)
    print(res.strip()[-1200:])
    os.remove(path)

if __name__ == "__main__":
    main()

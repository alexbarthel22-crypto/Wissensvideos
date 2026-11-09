# TikTok-Videos

Für jedes neue Video oder jede Änderung den Skill `tiktok-video` nutzen (`.claude/skills/tiktok-video/SKILL.md`). Immer Deutsch, alles mit HyperFrames.

Token sparsam einsetzen, ohne Qualität zu verlieren: bestehende Pipeline und Vorlagen wiederverwenden, gezielt lesen/editieren statt neu schreiben, nur Schlüsselmomente snapshotten, kurze Antworten (Details: Abschnitt „Effizient arbeiten“ im Skill).

Website muscheltal.de (Ordner `muscheltal/`, Netlify): Jeder Push mit Änderungen in `muscheltal/` kostet Netlify-Credits (ca. 15 pro Deploy). Website-Änderungen daher nur lokal committen und erst pushen, wenn der Nutzer „jetzt veröffentlichen“ sagt. Video-Änderungen dürfen normal gepusht werden (lösen keinen Build aus).

Videos und Homepage inhaltlich immer abgleichen: `MUSCHELTAL_FAKTEN.md` ist die gemeinsame Quelle. Vor jedem Muschel-Tal-Video oder jeder Homepage-Änderung lesen, bei Änderungen aktualisieren und den Nutzer auf inhaltliche Abweichungen hinweisen. Vorher `git pull`, weil Videos und Homepage in getrennten Chats bearbeitet werden können.

Nutzernamen: Der Nutzer schickt TikTok-Namen im Chat ohne „@“ (z. B. `vidafilipa`). Auf der Homepage und in den Daten stehen sie meist mit „@“ (z. B. `@vidafilipa`) – beim Suchen/Abgleichen immer ohne „@“ und ohne Groß-/Kleinschreibung vergleichen.

# 每日精读 A2 · Daily Reading A2

Daily English reading for junior-high students at A2 level (Cambridge KET standard). Same model as
[daily-news](https://github.com/Borami-hub/daily-news) (C1 / TOEFL), but with original
A2 coursebook / KET-exam-style texts (not news) and an extra Grammar module.

Web: https://borami-hub.github.io/daily-news-A2/

```
content/index.html              the app (single page, reads the files below at runtime)
content/days/index.json         list of published dates
content/days/<YYYY-MM-DD>.json  one day: 3 stories with words, questions, grammar, mind map, summary, speaking, writing
content/audio/<YYYY-MM-DD>/     mp3 narration referenced by the day file
kit/                            PIPELINE.md (day file format + steps), SYLLABUS.md (topics, genres, grammar order), validate.js, gen_audio.py
```

Modules per story: Words → Read → Questions (6 KET-style, 3 options) → Grammar (one junior-high
point, rule + examples from the story + 6 items) → Mind map → Summary → Speak → Write → Results.
Wrong grammar items, key points and words go into the spaced daily review.

**Daily flow.** A morning scheduled task picks 3 texts by `kit/SYLLABUS.md` (topic, genre and grammar
rotation), writes the day file per `kit/PIPELINE.md`, validates it, generates audio, and pushes to `main`.
`.github/workflows/pages.yml` then republishes the site.

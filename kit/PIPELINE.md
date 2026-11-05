# Daily Reading KET (A2): how to publish a day

Self-study reading app for junior-high students at **A2 / Cambridge KET** level. Same model as the
C1 news app (Borami-hub/daily-news), but the texts are not news: they are original A2 coursebook /
KET-exam-style texts chosen by `kit/SYLLABUS.md`, plus an extra Grammar module.

The page (`content/index.html`) reads `content/days/index.json` (list of dates) and
`content/days/<YYYY-MM-DD>.json` (one file per day) at runtime, plus audio from
`content/audio/<YYYY-MM-DD>/`. Publishing a day = adding those files. The page never needs editing.

- Web: https://borami-hub.github.io/daily-news-A2/ (GitHub Pages, deployed on every push to `main`)
- Student link (claude.ai artifact): https://claude.ai/artifact/DuQXGZyEbAd25j9gYzh6Ss
- Example day file: the first file in `content/days/` (read it to see the exact shape).

## Steps

1. Attach the repo with add_repo (owner `Borami-hub`, repo `daily-news-A2`, access `push`) and clone it.
2. Read `kit/SYLLABUS.md` and the last 10 day files, choose today's 3 topic + genre + grammar
   combinations by its rotation rules, and write `content/days/<date>.json` (format below).
3. `node kit/validate.js content/days/<date>.json` — fix every ERROR and rerun until OK. Treat WARN
   lines seriously (word counts, letter balance, long sentences).
4. `pip install --break-system-packages -q kokoro-onnx soundfile && cd content && python3 ../kit/gen_audio.py days/<date>.json`
   (downloads ~350 MB of voice model once; run in the background and wait).
5. Add the date to `content/days/index.json` → `{"days": [..., "<date>"], "updated": "<date>"}` (keep older dates).
6. Commit ("Add <date>") and push to `main`. The Pages workflow republishes the site.
7. Also republish the student link (Artifact tool: read it first, then publish to its `url` with `root` = `content`,
   `file_path` = `content/index.html`, `files` = the new day json, `days/index.json`, and the new mp3s).
8. Tell the teacher in Chinese, in one or two sentences, which three texts (title, genre, grammar point) are online.

## Language level (most important)

- **A2 / KET.** Use words from the Cambridge A2 Key vocabulary list wherever possible. Each story may
  add only the 8–10 taught words (`words`) above A2; explain everything else with easy words.
- Sentences short: average ≤ 14 words, none over 25. One idea per sentence.
- Tenses: present simple/continuous, past simple/continuous, present perfect, `will`/`going to`,
  can/must/should, comparatives/superlatives, `if` + present (first conditional). Avoid passive
  except simple `is made / was built`; avoid relative clauses without `who/which/that`.
- 250–350 words, 5–7 short paragraphs, in the shape of the chosen genre (see SYLLABUS.md).
- Written for 12–15-year-olds: friendly, concrete, everyday situations. Build the text so the
  grammar point appears naturally at least 3 times.

## Day file format (all student-facing text in English, no Chinese)

```
{
  "date": "YYYY-MM-DD",
  "headline": "≤ 60 chars, a fun title joining today's three texts",
  "teaser": "one sentence with 2–3 easy hook questions",
  "articles": [ ARTICLE, ARTICLE, ARTICLE ]
}
```

ARTICLE:

| field | content |
|---|---|
| `id` | `k<YYYYMMDD>-<1..3>` |
| `topic` | a topic name from SYLLABUS.md (e.g. School & study, Food & drink) |
| `genre` | Article / Story / Email / Interview / Three people / Notices & messages / Blog post |
| `title`, `dek` | short title (≤ 8 words); one easy sentence that makes students want to read |
| `sources` | `[]` for invented texts; `[{ "name": "Site", "url": "https://…" }]` when real facts were used |
| `paras` | 5–7 paragraph strings, 250–350 words in total |
| `words` | 8–10 items `{ w, level: "A2 word"\|"Topic word", pos, ipa, syl, def, ex }`. About half useful KET/A2-B1 words, half topic words. `w` appears in the story (plural/-ed/-ing OK). `syl` = the spelling split into syllables, joining back to `w` exactly (`["ex","pen","sive"]`); `ipa` uses `.` between syllables and `ˈ` before the stressed one, with the same number of syllables as `syl` (`/ɪkˈspen.sɪv/`) — the app shows the split and the stress. `def` = very easy English (≤ 12 words). `ex` = a NEW short example sentence containing `w` exactly. |
| `keySentences` | 3–5 `{ para, text, kind, note }`. `text` verbatim. `kind`: Main idea / Key details / Cause → effect / Time order / Opinion / Grammar to notice. `note`: 1 easy sentence. |
| `questions` | 6 KET reading questions, **3 options each**: `{ type, para, q, opts[3], a (0–2), why, evidence, optWhy[3] }`. Types (use at least 4 different ones): `Detail`, `Main idea`, `Word in context`, `Who / what does it mean?` (reference), `Right / Wrong / Doesn't say` (opts exactly `["Right","Wrong","Doesn't say"]`, at least 1 and at most 2 per story), `Writer's purpose`, `Feelings`, `What does the message say?` (Notices & messages genre: one notice per question, like KET Part 1). `evidence` verbatim from that paragraph (para 0 only for Main idea / Writer's purpose). `optWhy[i]`: start the answer with "Correct."; for wrong options say why in easy words (not in the story / the story says the opposite / true, but not the answer). Options must need the story to answer. Balance A/B/C across the day's 18 questions. |
| `grammar` | One junior-high grammar point found in the story: `{ point, rule, table?, examples, items }`. `point` ≤ 6 words (e.g. "Past simple: irregular verbs"). `rule` 2–3 easy sentences. `table` optional: up to 6 pairs `["go","went"]` or `["form","example"]`. `examples`: 2–4 `{ para, text, mark }`, `text` a verbatim sentence from that paragraph, `mark` the grammar words inside it (verbatim). `items`: exactly 6 — at least 2 `{ type: "mc", q, opts[3], a, why }` (q is a sentence with ___ ) and at least 2 `{ type: "fill", q, hint, a, why }` (q has ___ ; `hint` like "(go)"; `a` the exact answer, alternatives joined by " / "). Practice sentences are new (not from the story), about the story's topic or school life. `why` one easy sentence. Over a week, rotate points: past simple, present perfect, comparatives/superlatives, there is/are, can/must/should, will/going to, present continuous, countable/uncountable (some/any, much/many), prepositions of time/place, adverbs of frequency, first conditional, gerund vs to-infinitive, question words, possessives. |
| `kps` | 4–5 key points `{ id: "<article id>-k<n>", tag, fact, q, opts, a }`; `fact` one easy sentence, `q` with 3 options. Daily review. |
| `mindmap` | `{ center (≤ 3 words), question, branches: [4 × { title (≤ 2 words, e.g. Who / Where / Why / What next), paras: "1–2", blanks: [1–2 phrases ≤ 4 words], kps: [kp ids] }], distractors: [2 phrases ≤ 4 words: one not in the story, one wrong] }` |
| `summary` | `{ intro, model, options: [6 × { t, ok, why, type, para, evidence }] }` — 3 main ideas (type "main", ok true), 1 "detail", 1 "not" (para 0, evidence ""), 1 "contra". Each `t` ≤ 15 words. `model` = 2 sentences (≤ 30 words) using but / because / so. |
| `speak` | `{ p, hint, sec: 30–45 }` — KET Speaking-style personal question about the topic (e.g. "Do you like…? Why?"). `hint` gives 2 useful phrases. |
| `write` | `{ p, steps: [3 short steps = 3 things to write about], minWords: 25–35 }` — KET Writing Part 6 (email/message, 25+ words, 3 points) or Part 7 (short story, 35+ words). |

The audio map (`"audio": { text: path }`) is added by `gen_audio.py`; do not write it by hand.

## Voices

Each of the day's 3 texts (paragraphs, key sentences, grammar examples) is read by a different voice.
Words and their example sentences always use one clear American voice (af_heart), so pronunciation
stays the same model every day. `gen_audio.py` rotates 12 voices in a fixed order (US female, US male, UK female, UK male,
repeated three times), 3 per day, so the cycle repeats every 4 days; 2026-11-06 starts with voice 1. It also
writes each article's `voice` label (e.g. "British English · female"), shown on the reading page. Do not set
voices or `voice` by hand.

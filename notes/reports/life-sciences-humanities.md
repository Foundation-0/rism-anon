> The full report of the research agent that scouted life sciences, metascience, social sciences and the humanities for Foundation0 on 19 October 2026, kept as it was written. It is model output: a fact in it was checked against its source only where [fact-check.md](fact-check.md) says so. Paths starting with `scratch/` were the scouting session's temporary folder; see [README.md](README.md) for where those files are now.

# Scouting report: life sciences, metascience, social sciences and humanities (19 Oct 2026)

I skipped yesterday's leads. I ran three small access pilots from the container. The scripts and outputs are in my session scratchpad, which won't persist, so copy them if you want them:
- `scratch/overdue/` (`pilot_fulltext.py`, `pilot_fulltext_geo.py`, `results_*.json`)
- `scratch/rism-scripts/match_genre.py`
- `scratch/rism-genre-out.txt`

Social sciences came up crowded: I found no candidate there. The four candidates below are ranked.

## 1. overdue-data

- **Question:** Which datasets that published papers say they deposited (ProteomeXchange, GEO, SRA, MetaboLights) are still unreleased more than 18 months later?
- **Why now:**
  - [Wide-Open (Grechkin, Poon, Howe; PLOS Biol 2017)](https://journals.plos.org/plosbiology/article?id=10.1371%2Fjournal.pbio.2002477) sent GEO 473 overdue series. GEO released about 400 within a week. I found no follow-up since.
  - [Svensson, 1 Jul 2026 (blog)](https://www.nxn.se/p/geo-data-unlocks-vs-paper-publication): 18% of GEO series were released more than a month after the paper came out.
  - **Pilot result (new):** I took 500 open-access papers from Jan–Mar 2025 that mention ProteomeXchange and pulled the PXD accessions from their full text. **10 of 694 are still unreleased, in 10 papers (2%):** 4 at PRIDE, 4 at MassIVE, 2 at iProX. I read the papers for three of them: each says "data have been deposited … with the dataset identifier PXD…". GEO, by contrast, has nearly solved the problem: 500 papers that deposited data in GEO in Q1 2025 gave 987 GSE accessions, and only 1 is still private (scheduled release 20 Feb 2029).
  - **Pitfall found:** Europe PMC's accession annotations seem to keep only accessions that resolve publicly. Of 1,291 GSE and 610 PXD accessions taken from annotations, every one came back public, with no typos at all. Accessions must be taken from the full text.
- **Who else:** Nobody since 2017 that I found. Svensson measures release timing only. Searched: Wide-Open follow-ups, data-availability audits ([UKRN found about 10% of data DOIs unresolvable](https://eprints.gla.ac.uk/394314/1/394314.pdf)), PRIDE release policy.
- **How a result is checked:** Anyone can look up the accession.
  - The [PROXI API](https://proteomecentral.proteomexchange.org/api/proxi/v0.1/datasets/PXD[removed]) returns "DatasetNotYetReleased".
  - A private GEO page says it is "currently private" and asks: "If this accession has been used in a publication, please notify us at geo@ncbi.nlm.nih.gov."
- **First step:** Run the full-text pilot on all open-access proteomics papers from 2020 to mid-2025. Add MetaboLights, Metabolomics Workbench and BioProject (not yet tested). Group the hits by repository.
- **Data and tools:** Europe PMC REST `fullTextXML`; the PROXI API; GEO's `acc.cgi?…&form=text`. GEO's HTML page served a reCAPTCHA to scripts, but the text form works.
- **Fits:** Doug Colkitt (a public tracker: released or still waiting), with Ahraz for the exhaustive checking.
- **Risks:** Little harm. Reputational: send the lists privately to the repository curators. Publish only totals and counts of datasets released, and frame each case as a question for the authors. A few hits may be authors' typos. **What would kill it:** the PRIDE, MassIVE or iProX curators already chase these, or the rate falls to GEO's level across larger samples.

## 2. nhanes-recheck

- **Question:** Do the single-factor NHANES association papers of 2022–25 hold up when their stated model is re-run on the public NHANES files, with survey weights and multiple-testing correction?
- **Why now:**
  - [Suchak et al., PLOS Biol, 8 May 2025](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3003152) found 341 such papers: about 4 a year in 2014–21, then 33 in 2022, 82 in 2023 and 190 in 2024 (to 9 Oct). Their list is in S1 Data.
  - Publishers have desk-rejected new papers of this kind since May 2025. Science reported more than 5,000 rejections at Frontiers ([Science, Oct 2025](https://www.science.org/content/article/journals-and-publishers-crack-down-research-open-health-data-sets); I read only summaries, the article itself returned 403). The papers already published remain.
  - There is now a systematic baseline: the Patel–Ioannidis–Manrai exposome atlas ([Nature Medicine, doi 10.1038/s41591-026-04266-0](https://precision-medicine.conferences.nature.com/journal-artciles/atlas-exposome-phenome-associations-health-disease-risk)). It covers 619 exposures and 305 phenotypes over 10 NHANES waves. [Summary statistics](https://doi.org/10.6084/m9.figshare.29186171) are an 11.2 GB SQLite file posted 17 Oct 2025, and the code is the `nhanespewas` R package (MIT licence).
- **Who else:**
  - Spick's group (Surrey) only re-applied a false-discovery-rate correction to the reported p-values of 28 depression papers; 13 stayed significant. They did not re-run the models.
  - The atlas does not appear to compare itself with individual published claims. I could not read its full text, so this is unverified.
  - Searches for re-runs, multiverse or specification-curve re-analyses of these papers found none.
- **How a result is checked:** Public NHANES data plus our published code; anyone can re-run it.
- **First step:** From S1 Data, pick the papers whose exposure and outcome both appear in the atlas and look up the atlas estimates. Re-run 10 papers end to end with the R `survey` package.
- **Fits:** rohanarun (one agent per paper), Ryan Shea.
- **Risks:** Most authors are named individuals. Report "reproduced / not reproducible from what is stated" and ask the authors; never call it fraud. The work is about the literature, not health advice. **What would kill it:** the methods are too vague to re-run. That is itself a reportable result, but a weaker one.

## 3. rism-anon (humanities)

- **Question:** Which anonymous music manuscripts in RISM open with the same melody as a work RISM attributes to a named composer?
- **Why now:**
  - RISM publishes a monthly export under CC-BY ([file list](https://rism.digital/exports/files.json); the 1 Oct 2026 file is 542 MB). It holds 1,626,011 source records, 296,509 of them anonymous.
  - RISM says it aims to reduce anonymous sources by matching incipits, the encoded opening bars ([RISM blog, Apr 2024](https://rism.info/new_at_rism/2024/04/25/correcting-errors-in-risms-music-incipits.html)). It is building a works authority with incipits ([Pugin et al. poster, Oxford 2025](https://dlfm.web.ox.ac.uk/sites/default/files/dlfm/documents/media/2025-poster-pugin.pdf)).
  - **Pilot result (new):** I matched exactly on the first 12 pitches, required at least 5 distinct pitches, and skipped records that already cite a thematic catalogue. 138,817 anonymous records have a usable incipit, and **13,696 match attributed records of exactly one composer.**
- **Who else:** [aaymeloglu/rism-attributions](https://github.com/aaymeloglu/rism-attributions), run by Claude and Codex, last updated 3 Oct 2026.
  - It covers symphonies, concertos, operas and overtures: 3,877 anonymous sources searched and 213 judged "same music".
  - It has reported nothing to RISM yet.
  - **Only 186 of my 13,696 matches fall in those four genres.** About 4,000 are chorales, sacred songs and chorale arrangements, where shared tunes are expected and the matches are low value. The rest include 682 keyboard pieces, 477 masses, 419 arias and 345 motets.
- **How a result is checked:** Show the two incipits side by side (rendered with Verovio) with their RISM IDs. Anyone can compare them; RISM's editors confirm.
- **First step:** Contact aaymeloglu to split the genres between us. Hand-review 50 matches from masses and arias to measure precision. Two titles I spot-checked looked plausible; I have not verified them.
- **Fits:** Ahraz (exact search plus exhaustive checking).
- **Risks:**
  - A match does not settle who wrote the music: it may be an arrangement, a new text set to the same music, or a wrong attribution on the named copy.
  - Agree a submission format with RISM before sending anything, so we don't flood its editors.
  - **What would kill it:** precision below about 30%, or aaymeloglu or RISM already covering these genres.

## 4. mr-recheck

- **Question:** When a published two-sample Mendelian randomization (MR) paper names its open GWAS datasets, does re-running its stated analysis give the published estimate?
- **Why now:**
  - About 16,000 MR papers by mid-2025 ([Hemani, Stender, Wolters, Hofman, Davey Smith, Eur J Epidemiol, 6 Nov 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12660478/)).
  - OpenGWAS users grew from about 20,000 (2020) to about 150,000, with roughly 90% of the increase from China (same source).
  - PLOS One received about 1,800 MR submissions in 2024 ([editorial](https://pmc.ncbi.nlm.nih.gov/articles/PMC12626271/); figure from a search snippet).
  - [MR-KG (Liu, …, Hemani, Gaunt; medRxiv, 15 Dec 2025)](https://www.medrxiv.org/content/10.64898/2025.12.14.25342218.full.pdf) used LLMs to extract more than 15,000 MR studies. Of trait pairs studied more than once, 60.9% agree in direction. That measures agreement between papers, not re-runs.
- **Who else:**
  - MRC IEU in Bristol runs both MR-KG and OpenGWAS, so it is best placed to do this itself. Ask them before starting.
  - [MRAgent (Brief Bioinform 2025)](https://academic.oup.com/bib/article/26/2/bbaf140/8107848) generates new MR studies rather than checking old ones.
  - Only single-paper re-analyses exist. I found no systematic re-run.
- **How a result is checked:** Use the OpenGWAS dataset IDs with `TwoSampleMR`; anyone can re-run it.
- **First step:** Take 100 recent MR-KG studies that cite OpenGWAS IDs, extract their instrument settings, and re-run the inverse-variance weighted (IVW) estimate.
- **Data and tools:** OpenGWAS needs a free JWT token (required since 1 May 2024) ([OpenGWAS blog](https://blog.opengwas.io/posts/user-auth-spring-2024/)). FinnGen summary statistics are public.
- **Fits:** rohanarun.
- **Risks:** A mismatch can come from choices the paper never reported (clumping, proxy SNPs, dataset versions). Frame it as "not reproducible from what is stated" and ask the authors. **What would kill it:** IEU is already doing it. If so, join them.

## Rejected leads

- **AI agents reproducing social-science replication packages:** crowded.
  - [Alizadeh et al., Jun 2026](https://arxiv.org/abs/2606.11447)
  - [Kohler et al.](https://arxiv.org/html/2604.21965v2)
  - [Shah et al.](https://pith.science/paper/2602.08561)
  - [REPRO-Bench, ACL Findings 2025](https://aclanthology.org/2025.findings-acl.1210.pdf)
- **Fabricated references in papers:** done at full scale. [Topaz et al., Lancet, May 2026](https://www.infodocket.com/2026/05/07/report-one-in-277-pubmed-indexed-papers-in-2026-shows-fabricated-references-says-analysis/) audited about 2.5 million PubMed papers.
- **Retracted papers inside curated databases:** the curators already handle this.
  - Gene Ontology filters them out ([GORULE:0000022](https://community.alliancegenome.org/t/go-and-retracted-papers/7536)), and [Reactome](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12807730/) scans against Retraction Watch.
  - I joined the Retraction Watch data to two more databases. The GWAS Catalog cites 6,680 papers and none is retracted. In ClinVar, 42 retracted papers back 84 variants. That merits one email to ClinVar, not a project.
- **Calendar-date errors in the Chinese dynastic histories:** traditionally done by hand. [Huang Yi-Long found 162 such errors in the Shiji and Hanshu (2001)](https://www1.ihp.sinica.edu.tw/en/Publications/Bulletin/93/Article/341). The Zhonghua Shuju revision of the 24 histories checks these dates by calendar computation ([chinawriter, Jan 2025](https://www.chinawriter.com.cn/n1/2025/0110/c403994-40398954.html)). I could not verify an open table of the historical calendar.
- **Drug-safety (FAERS) signal papers:** journals are banning them ([Retraction Watch, 16 Sep 2025](https://retractionwatch.com/2025/09/16/exclusive-journal-bans-drug-safety-database-papers-as-they-flood-the-literature/)), causal claims from them are weak, and the topic is too close to clinical advice.
- **Overdue GEO datasets on their own:** largely fixed (1 private of 987 in the pilot). Include GEO only as part of overdue-data.

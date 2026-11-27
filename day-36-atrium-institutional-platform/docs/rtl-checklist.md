# Arabic / RTL checklist (test every page, list form and app screen)

- Site created in the right default language (it can't be changed later). English default + Arabic as an extra
  language on communication sites; Arabic default for Arabic-first team sites.
- Users set their language in their Microsoft 365 profile; test with one English and one Arabic account.
- Page translation: translated pages are copies you translate and publish; republish the default page after.
- Navigation, site title, footer: translate them in the multilingual settings.
- Mixed text: references like `OUT-CI-2027-00042` inside Arabic sentences can flip. Keep references in their
  own column / span.
- Dates and numbers: decide Western vs Arabic-Indic digits per audience and stick to it.
- Power Apps: set the app's layout direction from the user's language; check icons with arrows.
- Exports: write CSVs with a UTF-8 BOM so Excel shows Arabic correctly.

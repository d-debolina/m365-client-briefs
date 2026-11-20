# Which limit am I hitting? (CARGO triage)

| Symptom | Likely limit | Where to fix |
|---|---|---|
| Uploads fail above ~5 MB, even though the form says 50 MB | **Environment email attachment limit** (System settings → Email → Maximum file size). Notes storage can't exceed it | Power Platform admin centre → environment → Settings → Email. Max for notes storage = **90 MB** |
| Fails above the form's own limit | Form setting **Upload size limit per file (KB)** / Basic Form Metadata **Maximum File Size (KB)** | Design studio form settings or Portal Management app |
| Some file types rejected | **Accept MIME types / File types allowed** | Same place |
| Fails on files of 100 MB+ with Notes storage | Notes max (90 MB) | Switch to **Azure Blob Storage** (up to **10 GB** per file) |
| "To access more controls for file upload, update the Dataverse Base portal package" | Old portal package | Update the package to 9.3.2405.x or later; site runtime 9.6.5.1+ |
| Upload "succeeds" but the file lands in Dataverse, not Azure | Blob processes deactivated after migration | Activate *AzureBlobStorageEnabled*, *Azure Blob Storage Url*, *Generate Shared Access Signature* |
| Attachments added via the timeline/comments are always in Dataverse | Portal comments don't use Blob | Use Basic Form Metadata (Notes) for uploads; timeline needs `FileStorage/*` site settings |
| Internal users can't see Blob files in the model-driven app | Missing web resource / CORS | Add the Azure Storage web resource + storage CORS rule |

# CARGO test plan

| File | Notes storage (5 MB email limit) | Notes storage (limit raised to 90 MB) | Azure Blob storage |
|---|---|---|---|
| 04MB.pdf | ✅ | ✅ | ✅ |
| 12MB.pdf | ❌ (the client's bug) | ✅ | ✅ |
| 80MB.zip | ❌ | ✅ | ✅ |
| 120MB.zip | ❌ | ❌ (over 90 MB) | ✅ |
| 600MB.mp4 | ❌ | ❌ | ✅ |
| bad-type.exe | ❌ type | ❌ type | ❌ type |

Also test: anonymous vs authenticated user, download from the portal, and preview from the model-driven app.

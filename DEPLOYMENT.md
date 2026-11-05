# Deployment Guide: Vercel + Render

This repository has a Vite frontend and a separate Flask backend. Deploy the frontend to Vercel and the Python API to Render. Use the repository root for Vercel and the top-level `backend/` directory for Render; `jansakshi/` and `jansakshi_source/` contain duplicate project files and are not the paths used by the root Vite app.

## 1. Push the project to GitHub

Commit and push the project to a GitHub repository. Do not commit `.env` files or API keys. The repository's `.gitignore` already excludes `.env*` files other than `.env.example`.

## 2. Deploy the Flask API to Render

1. In Render, choose **New + > Web Service** and connect the GitHub repository.
2. Set **Root Directory** to `backend`.
3. Choose **Python** as the runtime.
4. Set the build command to:

   ```sh
   pip install -r requirements.txt gunicorn
   ```

5. Set the start command to:

   ```sh
   gunicorn app:app --bind 0.0.0.0:$PORT
   ```

6. Add these environment variables in the Render service settings:

   | Key | Value |
   | --- | --- |
   | `GEMINI_API_KEY` | Your Google Gemini API key |
   | `GEMINI_MODEL` | Optional; defaults to `gemini-2.5-flash` in the backend |

7. Create the service and wait for the deployment to finish. Copy its public URL, for example `https://your-service.onrender.com`.

Check that `https://your-service.onrender.com/api/health` returns JSON and reports the backend online. The health response also indicates whether the Gemini key is configured.

## 3. Route frontend API requests through Render

The frontend calls relative `/api/...` URLs. The proxy in `vite.config.ts` is for local development only, so production needs a Vercel rewrite.

Create `vercel.json` in the repository root, replacing the example host with the Render URL from the previous step:

```json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://your-service.onrender.com/api/:path*"
    }
  ]
}
```

Commit and push this file. The rewrite keeps browser requests on the Vercel domain while forwarding API traffic to Render.

## 4. Deploy the frontend to Vercel

1. In Vercel, choose **Add New > Project** and import the same GitHub repository.
2. Set the project **Root Directory** to the repository root.
3. Use these build settings:

   | Setting | Value |
   | --- | --- |
   | Framework Preset | Vite |
   | Build Command | `npm run build` |
   | Output Directory | `dist` |
   | Install Command | `npm install` |

4. No Gemini key is needed in Vercel; keep it only in Render's environment settings.
5. Deploy. Vercel will redeploy when the `vercel.json` change is pushed.

## 5. Verify the deployment

- Open the Vercel URL and confirm the citizen portal loads.
- Open `https://your-vercel-domain/api/health`; it should return the Render health response through the rewrite.
- Submit a test complaint and confirm the API response contains a complaint ID.
- Check the Render logs if the API reports an error. On a free Render instance, the first request after inactivity may take longer while the service starts.

## Current limitations to resolve

- The deployed portal in `public/js/app.js` calls `/api/ai/analyze-complete` and `/api/ai/predictive-insights`, but the top-level `backend/app.py` currently provides neither route. Complaint submission falls back to `/api/complaints`, so basic registration may work while AI triage and predictive insights do not. The guide deploys the current code; it does not add those missing API features.
- The backend stores SQLite data at `backend/jansakshi.db`. Render's default filesystem is ephemeral, so complaint records can be lost when the service is replaced or restarted. The current backend does not read a configurable database path. For durable production data, first move the app to a managed database or update it to use a Render persistent disk mounted at the database path.
- The root Vite build serves `index.html` and files under `public/`. It does not automatically publish every similarly named HTML file at the repository root or under the duplicate project folders. Check any linked pages against the deployed site.
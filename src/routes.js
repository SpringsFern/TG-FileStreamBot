import { epoch, shorten, getTemplate, formatMap, humanbytes } from "./utils";
import { CONFIG } from "./config"

export function registerRoutes(app) {
	app.get("/", c => {
		return c.redirect("https://springsfern.in")
	});
	// app.get("/status", status);
	app.get("/play/:msg_id", renderPlayer);
	// app.get("/loading/:id", ads_page);
	app.get("/dl/:msg_id", Redirect);

	app.get("/ads.txt", c => {
		return c.body(c.env.ADS)
	})

}

async function Redirect(c) {
  const queryParams = c.req.query();
  let messageId, secureHash;
  messageId = parseInt(c.req.param("msg_id"), 10);
  secureHash = queryParams.hash || null;
  if (!messageId || !secureHash) {
    return c.text("Invalid URL: messageId and secureHash are required", 400);
  }

	let link = `${c.env.URL}/play/${messageId}?hash=${secureHash}`;

	if ( c.env.SHOW_ADS) {
		link = await shorten(c.env, link);
	}

	return c.redirect(link);
}

async function renderPlayer(c) {
	let messageId, secureHash;
	const queryParams = c.req.query();
	messageId = parseInt(c.req.param("msg_id"), 10);
	secureHash = queryParams.hash || null;
	if (!messageId || !secureHash) {
	  return c.text("Invalid URL: messageId and secureHash are required", 400);
	}

	const link = `${messageId}?hash=${secureHash}&d=true`

	try {
        const response = await fetch(c.env.DL_URL2 + link, { method: 'HEAD' });

        if (!response.ok) {
			const response = await fetch(c.env.DL_URL + link, { method: 'GET' });
			if (!response.ok) {
				return c.json({ error: 'Failed to fetch file info' }, 400);
			}
        }

        // Extract file details from headers
        const contentType = response.headers.get('Content-Type') || 'Unknown';
        const contentLength = response.headers.get('Content-Length') || 'Unknown';
        const contentDisposition = response.headers.get('Content-Disposition');

		const file_type = contentType.split("/")[0] || "Unknown"
        let fileName = 'Unknown';
        if (contentDisposition) {
            const match = contentDisposition.match(/filename="?([^"]+)"?/);
            if (match) {
                fileName = match[1];
            }
        }

		let player = null
		if (["audio", "video"].includes(file_type)) {
			player = file_type
		}
	
		const res = formatMap(await getTemplate(c.env, "dl"), {
			"hides": player ? "" : "<!--",
			"hidee": player ? "" : "-->",
			"tag": player,
			"source_link": player ? link : null,
			"download_link": c.env.DL_URL + link,
			"download_link2": c.env.DL_URL2 + link,
			"file_name": fileName,
			"file_size": humanbytes(contentLength),
			"vlc_link": `vlc://${c.env.DL_URL.replace('https://', '')}${link}`,
			"mx_link": `intent:${c.env.DL_URL + link}#Intent;package=com.mxtech.videoplayer.ad;end`,
			// "adsense": c.env.BLOG ? '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9019718369052772"crossorigin="anonymous"></script>' : ''
			"adsense": '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9019718369052772"crossorigin="anonymous"></script>'
		})
		return c.html(res);

    } catch (error) {
        return c.json({ error: 'Error fetching file info', details: error.message }, 500);
    }
}

import { epoch, shorten, getTemplate, formatMap, humanbytes } from "./utils";
import { CONFIG } from "./config"
import FileData from "./metadata"

export function registerRoutes(app) {
	app.get("/", c => {
		return c.redirect("https://springsfern.in")
	});
	// app.get("/status", status);
	app.get("/play/:id", renderPlayer);
	app.get("/loading/:id", ads_page);
	app.get("/dl/:msg_id", Redirect)
	app.get("/dl/:msg_id/:name", Redirect)
	app.get("/ads.txt", c => {
		return c.body(c.env.ADS)
	})

}

async function Redirect(c) {
	const name = c.req.param("name") || "None";
	const msgId = c.req.param("msg_id");
	const mimeType = c.req.query("mime") || "file";
	const size = c.req.query("size") || 0;
	const createTime = parseInt(c.req.query("time")) || 0;
	const file = new FileData(msgId, mimeType, size, name)
	const filestr = file.encode()

	if (createTime && epoch() >= createTime + CONFIG.EXPIRE_TIME) {
		return c.text("Link Expired", 410);
	}

	let link = `${c.env.URL}/play/${filestr}`;

	if ((!createTime || createTime + CONFIG.ONE_DAY >= epoch()) && !c.env.BLOG_MODE) {
		// link = await shorten(c.env, link);
		link = `${c.env.URL}/loading/${filestr}`;
	}
	if (c.env.BLOG_MODE) {
		console.log("Executed")
		const blogs = ["blog1", "blog2"];
		const redirectUrl = `${c.env.URL}/${blogs[Math.floor(Math.random() * blogs.length)]}?url=${encodeURIComponent(link)}`;
		return c.redirect(redirectUrl);
	}

	return c.redirect(link);
}

async function ads_page(c) {
	const id = c.req.param("id")
	if (id.length < 28) {
		return c.notFound()
	}
	const decoded = FileData.decode(c.req.param("id"));

	const res = formatMap(await getTemplate(c.env, "ads_page"), {
		"name": decoded.name,
		"size": humanbytes(decoded.size),
		"mime": decoded.mimeType,
		"url": `${c.env.URL}/play/${c.req.param("id")}`,
		"adsense": '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9019718369052772"crossorigin="anonymous"></script>'
	})
	return c.html(res);
}

async function renderPlayer(c) {
	const id = c.req.param("id")
	if (id.length < 28) {
		return c.notFound()
	}
	const decoded = FileData.decode(c.req.param("id"));
	console.log(decoded)
	const file_type = decoded.mimeType.split("/")[0] || "Unknown"

	const link = `dl/${decoded.msgId}/${decoded.name}`

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
		"file_name": decoded.name,
		"file_size": humanbytes(decoded.size),
		"vlc_link": `vlc://${c.env.DL_URL.replace('https://', '')}${link}`,
		"mx_link": `intent:${c.env.DL_URL + link}#Intent;package=com.mxtech.videoplayer.ad;end`,
		// "adsense": c.env.BLOG ? '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9019718369052772"crossorigin="anonymous"></script>' : ''
		"adsense": '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9019718369052772"crossorigin="anonymous"></script>'
	})
	return c.html(res);
}

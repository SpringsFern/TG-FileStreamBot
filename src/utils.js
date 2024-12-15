import fetch from "node-fetch";  // Ensure fetch support if needed

export function epoch() {
	return Math.floor(Date.now() / 1000);
}

export async function shorten(env, shortLink) {
	const response = await fetch(`${env.API_BASE_URL}/api?api=${env.API_KEY}&url=${shortLink}`);

	const shortenedUrl = await response.json();
    console.log(shortenedUrl)
	if (shortenedUrl.status === "success") {
		return shortenedUrl.shortenedUrl;
	}
	return shortLink;  // Return original if not successful
}

export async function getTemplate(env, templateName) {
    const template = await env.TEMPLATE_STORE.get(templateName);
    if (!template) {
        throw new Error(`Template ${templateName} not found`);
    }
    return template;
}

export function formatMap(template, values) {
	return template.replace(/\{\{(\w+)\}\}/g, (match, key) => {
	  return key in values ? values[key] : match;
	});
  }

export function humanbytes(size){
	// https://stackoverflow.com/a/49361727/4723940
	// 2**10 = 1024
	if (!size){
		return ""
	}
	const power = 2**10
	let n = 0
	const Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
	while (size > power){
		size /= power
		n += 1
	}
	return Math.round(size, 2) + " " + Dic_powerN[n] + 'B'
}
import { apiHost } from "@/env.ts";

function urlPathToWsUrl(urlPath) {
  let _url;
  // Use wss:// if running on https://
  const scheme = window.location.protocol === "https:" ? "wss" : "ws";
  const baseUrl = `${scheme}://${apiHost}`;
  if (urlPath === undefined) {
    _url = baseUrl;
  } else {
    // Support relative URLs
    if (urlPath[0] == "/") {
      _url = `${baseUrl}${urlPath}`;
    } else {
      _url = urlPath;
    }
  }
  return _url;
}

export { urlPathToWsUrl };

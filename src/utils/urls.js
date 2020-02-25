function pathToWsUrl(urlPath) {
  let _url;
  // Use wss:// if running on https://
  const scheme = window.location.protocol === "https:" ? "wss" : "ws";
  const baseUrl = `${scheme}://${window.location.host}`;
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

export { pathToWsUrl };

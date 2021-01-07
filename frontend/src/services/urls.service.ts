// borrowed from django-channels
// see: https://github.com/nathantsoi/vue-native-websocket/issues/44#issuecomment-386423806
export const getWsUrl = (url: string): string => {
  let _url;
  // Use wss:// if running on https://
  const scheme = window.location.protocol === "https:" ? "wss" : "ws";
  const base_url = `${scheme}://${window.location.host}`;
  if (url === undefined) {
    _url = base_url;
  } else {
    // Support relative URLs
    if (url[0] == "/") {
      _url = `${base_url}${url}`;
    } else {
      _url = url;
    }
  }
  return _url;
};

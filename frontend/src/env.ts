export const appName = "UVP Interactive";
export const apiHost =
  window.location.host === "frontend" ? "backend" : window.location.host;
export const apiUrl = `${window.location.protocol}//${apiHost}`;
console.log(apiUrl);

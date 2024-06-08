
function createMeets() {
    const roomID = getUrlParams(window.location.href)['roomID'] || (Math.floor(Math.random() * 10000) + "");
    const userID = Math.floor(Math.random() * 10000) + "";
    const userName = "userName" + userID;
    const appID = 1146201911;
    const serverSecret = "a86b408d05443e7ee8aae7bfe0c02547";
    const kitToken = ZegoUIKitPrebuilt.generateKitTokenForTest(appID, serverSecret, roomID, userID, userName);
    //console.log(appID, serverSecret, roomID, userID, userName);
}

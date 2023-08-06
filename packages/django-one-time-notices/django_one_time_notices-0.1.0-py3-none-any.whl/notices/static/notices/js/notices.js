(
    function () {
        const clear = document.getElementById('noticesClear');
        if (clear) {
            document.cookie = "notices_seen=; Max-Age=-99999999;"
            clear.remove()
        };
    }
)();

var noticesCookie = {
    createCookie: function (value, days) {
        var date = new Date(),
        expires = '';
        if (days) {
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toGMTString();
        } else {
        expires = "";
        }
    
        var secureString = "";
        if (window.isSecureContext) {
        secureString = "; Secure";
        }
    
        document.cookie = "notices_seen" + "=" + value + expires + "; path=/" + secureString;
    },
    
    setCookie: function (version) {
        this.createCookie(version, 10 * 365);
        this.hidenoticedModal()
    },
    
    hidenoticedModal: function () {       
        document.getElementById('noticesModal').remove();
        document.getElementById('noticesModalFader').remove();
    },
};

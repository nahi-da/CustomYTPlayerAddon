// プレイリストのID（ここを再生したいIDに変えてください。）
const PlaylistId = '書き換える部分';

// エラーページにあるdiv要素を削除
var rem_elem = document.getElementById('error-page');
rem_elem.remove();

// viewportの呪文をheadに書き込む
var meta = document.createElement('meta');
meta.name = "viewport";
meta.content = "width=device-width, initial-scale=1";
document.head.appendChild(meta);

// iframeを挿入するdiv
var video_container = document.createElement('div');
video_container.id = 'video-container'
video_container.style = "position: absolute; top: 0; left: 0; width: 100%; height: 100%;";
document.body.appendChild(video_container);

// APIによってiframeに置き換えられるdiv
var iframe = document.createElement('div');
iframe.id = "player";
iframe.style = "position: absolute; top: 0; left: 0; width: 100%; height: 100%;";
video_container.appendChild(iframe);

// エラーページに直接書き込むスクリプト
var myscript_elem = document.createElement('script');
var myscript_content = `
var player;
var title;
var title_elem = document.querySelector('title');
function onYouTubeIframeAPIReady() {
    player = new YT.Player('player', {
        width: '100%',
        height: '100%',
        playerVars: {
            listType: 'playlist',
            list: \'${PlaylistId}\',
            autoplay: 1,
        },
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        }
    });
}

function onPlayerReady(event) {
    event.target.setShuffle({'shufflePlaylist' : true});
    event.target.playVideoAt(0);
}

function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.PLAYING) {
        title = event.target.getVideoData()['title'];
        title_elem.innerText = title;
    }
}

const resizeObserver = new ResizeObserver(entries => {
    for (const entry of entries) {
        if (entry.target === document.documentElement) {
            // 要素のサイズが変わった時の処理を行う
            resize();
        }
    }
});

resizeObserver.observe(document.documentElement);

function resize() {
    var ch = document.documentElement.clientHeight;
    var cw = document.documentElement.clientWidth;
    var vc = document.getElementById('video-container');
    if (ch > cw / 16 * 9) {
        vc.style = "position: absolute; top: 0; left: 0; width: 100%;"
        vc.style['height'] = "0";
        vc.style["padding-bottom"] = "56.25%";
    } else {
        vc.style = "position: absolute; top: 0; left: 0; width: 100%;"
        vc.style['height'] = \`\$\{ ch \}px\`;
        vc.style['padding-bottom'] = "0";
    }
}
`
myscript_elem.textContent = myscript_content;
document.body.appendChild(myscript_elem);

// IFrame APIのスクリプト
var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
document.body.appendChild(tag);

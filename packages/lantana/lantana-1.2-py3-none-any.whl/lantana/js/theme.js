//Materialテーマ相互運用機能

//該当するクラスを置換するメソッド
function replace_class(base,to){
    document.querySelectorAll('.'+base).forEach(element => element.classList.replace(base,to));
}
function add_class(base,to){
    document.querySelectorAll('.'+base).forEach(element => element.classList.add(to));
}

//MaterialのAdmonitionをAlertに置換
replace_class('admonition','alert');
replace_class('admonition-title','alert-heading');

//MaterialのAdmonition色をAlert色に置換
add_class('note','alert-primary');
add_class('abstract','alert-secondary');
add_class('info','alert-info');
add_class('tip','alert-warning');
add_class('success','alert-success');
add_class('question','alert-secondary');
add_class('warning','alert-warning');
add_class('failure','alert-danger');
add_class('danger','alert-danger');
add_class('bug','alert-warning');
add_class('example','alert-dark');
add_class('quote','alert-light');

//コードブロックのコピーアイコンの定義
const ICON_COPY = 'bi-clipboard';
const ICON_COPY_CHECK = 'bi-clipboard-check';

//コードブロックにコピーボタンを追加
$(".highlight").addClass("bg-light");
$(".highlight").addClass("position-relative");
$(".highlight").prepend('<button onclick="copy_btn_clicked(this)" class="btn btn-light position-absolute top-0 end-0"><i class="bi '+ICON_COPY+'"></i></button>');

//コードブロックのコピーボタンが押されたときの処理
function copy_btn_clicked(btn){
    const selection = window.getSelection();
    const code = btn.parentNode;
    selection.selectAllChildren(code);
    document.execCommand('copy');
    btn.querySelector('.'+ICON_COPY).classList.add('text-success');
    btn.querySelector('.'+ICON_COPY).classList.replace(ICON_COPY,ICON_COPY_CHECK);
}

//表をBootstrap仕様に
$("table").addClass("table");

//引用をBootstrap仕様に
$("blockquote").addClass("blockquote");

//画像をBootstrap仕様に
$("img").addClass("img-fluid");
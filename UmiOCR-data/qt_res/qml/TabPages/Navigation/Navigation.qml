// ================================================
// =============== 导航页（新标签页） ===============
// ================================================

import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import ".."
import "../.."
import "../../Widgets"

TabPage {

    // =============== 逻辑 ===============

    id: naviPage
    // 页面信息存储
    ListModel { id: pageModel }
    // 动态变化的简介文本
    property string introText: ""
    // 初始简介（欢迎词）
    property string welcomeText: `# `+qsTr("欢迎使用 Umi-OCR")+`

## 👈 `+qsTr("请选择功能页")+`



#### Umi-OCR `+qsTr("主页")+`

[${UmiAbout.homepage}](${UmiAbout.homepage})

#### `+qsTr("作者")+`

${getTD(UmiAbout.authors)}

#### `+qsTr("译者")+`

${getLocalizationTable()}`

    function getTD(as) { // 传入人员列表，生成人员的 <a> 标签
        let t = "", l = as.length-1
        for(const i in as) {
            const a = as[i]
            t += `<a href="${a.url}"><font color="${theme.specialTextColor}">${a.name}</font></a>`
            if(i < l) t += " | "
        }
        return t
    }
    function getLocalizationTable() { // 生成 译者信息
        let table = "<table>"
        for(const lang in UmiAbout.localization) {
            const info = UmiAbout.localization[lang]
            let t = `<tr><td>${lang}\t</td><td>${getTD(info)}</td></tr>`
            table += t
        }
        table += "</table>"
        return table
    }

    // 初始化数据
    Component.onCompleted: initData()
    function initData() {
        introText = welcomeText
        pageModel.clear()
        const f = qmlapp.tab.infoList
        // 遍历所有文件信息（排除第一项自己）
        for(let i=1,c=f.length; i<c; i++){
            pageModel.append({
                "title": f[i].title,
                "intro": f[i].intro,
                "infoIndex": i,
            })
        }
    }


    // =============== 布局 ===============

    DoubleRowLayout {
        anchors.fill: parent
        initSplitterX: size_.line * 15
        
        // =============== 左侧，展示所有标签页名称 ===============
        leftItem: Panel {
            anchors.fill: parent

            Item {
                id: topLable
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.margins: size_.spacing
                height: size_.line * 2.5
                Text_ {
                    anchors.centerIn: parent
                    text: qsTr("功能页")
                    color: theme.subTextColor
                }
                MouseAreaBackgroud {
                    onHoveredChanged: naviPage.introText = naviPage.welcomeText
                }
            }

            ScrollView {
                id: scrollView
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.top: topLable.bottom
                anchors.margins: size_.spacing
                clip: true

                Column {
                    anchors.fill: parent
                    spacing: size_.spacing * 0.5

                    Repeater {
                        model: pageModel
                        Button_ {
                            text_: title
                            width: scrollView.width
                            height: size_.line * 2.5

                            onHoveredChanged: {
                                naviPage.introText = intro
                            }
                            onClicked: {
                                let i = qmlapp.tab.getTabPageIndex(naviPage)
                                if(i < 0){
                                    console.error("【Error】导航页"+text+"未找到下标！")
                                }
                                qmlapp.tab.changeTabPage(i, infoIndex)
                            }
                        }
                    }
                }
            }
        }

        // =============== 右侧，展示功能简介 ===============
        rightItem: Panel{
            anchors.fill: parent
            
            MarkdownView {
                id: introView
                anchors.fill: parent
                anchors.margins: size_.spacing * 2
                text: introText
            }
        }
    }
}
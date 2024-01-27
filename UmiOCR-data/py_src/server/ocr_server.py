import json

from .bottle import request
from ..mission.mission_ocr import MissionOCR
from ..utils.utils import initConfigDict


# 获取ocr配置字典
def _get_ocr_options():
    opts = {}
    # OCR 的参数
    ocr_opts = MissionOCR.getLocalOptions()
    ocr_opts = initConfigDict(ocr_opts)
    for key in ocr_opts:
        opts[f"ocr.{key}"] = ocr_opts[key]
    # 排版解析的参数
    opts[f"tbpu.parser"] = {  # TODO: 新排版解析的HTTP接口数据
        "title": "排版解析",
        "default": "MergeLine",
        "optionsList": [
            ["MergeLine", "单行"],
            ["MergePara", "多行-自然段"],
            ["MergeParaCode", "多行-代码段"],
            ["MergeLineVrl", "竖排-从右到左"],
            ["MergeLineVlr", "竖排-从左到右"],
            ["None", "不做处理"],
        ],
    }
    return opts


# 路由函数
def init(UmiWeb):
    @UmiWeb.route("/api/ocr/get_options")
    def _get_options_json():
        opts = _get_ocr_options()
        res = json.dumps(opts)
        return res

    """
    执行OCR，方法：POST
    参数：
    "base64": "", # 必填
    "options": {}, # 选填，内容与 _get_options 的对应。
    """

    @UmiWeb.route("/api/ocr", method="POST")
    def _ocr():
        try:
            data = request.json
        except Exception as e:
            return json.dumps({"code": 800, "data": f"请求无法解析为json。"})
        if not data:
            return json.dumps({"code": 801, "data": f"请求为空。"})
        if "base64" not in data:
            return json.dumps({"code": 802, "data": f"请求中缺少 base64 字段。"})
        if "options" not in data:
            data["options"] = {}
        elif not type(data["options"]) is dict:
            return json.dumps({"code": 803, "data": f"请求中 options 字段必须为字典。"})
        # 补充缺失的默认参数
        try:
            opt = data["options"]
            default = _get_ocr_options()
            for key in default:
                if key not in opt:
                    opt[key] = default[key]["default"]
        except Exception as e:
            return json.dumps({"code": 804, "data": f"options 解释失败。 {e}"})
        # 同步执行
        resList = MissionOCR.addMissionWait(opt, {"base64": data["base64"]})
        res = resList[0]["result"]
        res = json.dumps(res)
        return res


"""
const url = "http://127.0.0.1:1224/api/ocr";
const data = {
    // 必填
    "base64": "iVBORw0KGgoAAAANSUhEUgAAAC4AAAAXCAIAAAD7ruoFAAAACXBIWXMAABnWAAAZ1gEY0crtAAAAEXRFWHRTb2Z0d2FyZQBTbmlwYXN0ZV0Xzt0AAAHjSURBVEiJ7ZYrcsMwEEBXnR7FLuj0BPIJHJOi0DAZ2qSsMCxEgjYrDQqJdALrBJ2ASndRgeNI8ledutOCLrLl1e7T/mRkjIG/IXe/DWBldRTNEoQSpgNURe5puiiaJehrMuJSXSTgbaby0A1WzLrCCQCmyn0FwoN0V06QONWAt1nUxfnjHYA8p65GjhDKxcjedVH6JOejBPwYh21eE0Wzfe0tqIsEkGXcVcpoMH4CRZ+P0lsQp/pWJ4ripf1XFDFe8GHSHlYcSo9Es31t60RdFlN1RUmrma5oTzTVB8ZUaeeYEC9GmL6kNkDw9BANAQYo3xTNdqUkvHq+rYhDKW0Bj3RSEIpmyWyBaZaMTCrCK+tJ5Jsa07fs3E7esE66HzralRLgJKp0/BD6fJRSxvmDsb6joqkcFXGqMVVFFEHDL2gTxwCAaTabnkFUWhDCHTd9iYrGcAL1ZnqIp5Vpiqh7bCfua7FA4qN0INMcN1+cgCzj+UFxtbmvwdZvGIrI41JiqhZBWhhF8WxorkYPpQwJiWYJeA3rXE4hzcwJ+B96F9zCFHC0FcVegghvFul7oeEE8PvHeJqC0w0AUbbFIT8JnEwGbPKcS2OxU3HMTqD0r4wgEIuiKJ7i4MS16+og8/+bPZRPLa+6Ld2DSzcAAAAASUVORK5CYII=",
    "options": {
        "ocr.angle": false,
        "ocr.language": "简体中文",
        "ocr.maxSideLen": 1024,
        "tbpu.parser": "MergeLine",
    }
};

fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error(error);
    });



const url = "http://127.0.0.1:1224/api/ocr/get_options";
fetch(url, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        },
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error(error);
    });
"""

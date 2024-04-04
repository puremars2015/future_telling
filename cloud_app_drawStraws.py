import functions_framework
from datetime import datetime
import os
try:
    from flask import Flask, request, jsonify, render_template
    from openai import OpenAI
except:
    os.system('python -m pip install flask')
    os.system('python -m pip install openai')
    from flask import Flask, request, jsonify, render_template
    from openai import OpenAI

import random

@functions_framework.http
def hello_http(request):

    # For more information about CORS and CORS preflight requests, see:
    # https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request

    # Set CORS headers for the preflight request
    if request.method == "OPTIONS":
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }

        return ("", 204, headers)

    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    problemSituation = request.json.get('problemSituation')
    if not problemSituation:
        return (jsonify({'signPoems': '無事所求，不必問，自有安排，自有分配。'}), 200, headers)

    # 使用當天的日期和基數生成隨機種子，以確保每天的運氣是不同的
    random.seed(int(datetime.now().timestamp()))
    
    # 生成一個0到100之間的隨機數，作為運氣指數
    luck_index = random.randint(1, 65)

    # 從future_telling.db取得資料,亂數取出一筆籤詩
    signPoems = GetCardById(luck_index)

    signPoems[1].encode('big5')


    return (jsonify({'signPoems': signPoems[1]}), 200, headers)


futune_lots = [[1, "\u65e5\u51fa\u4fbf\u898b\u98a8\u96f2\u6563,\u5149\u660e\u6e05\u6de8\u7167\u4e16\u9593,\u4e00\u5411\u524d\u9014\u901a\u5927\u9053,\u842c\u4e8b\u6e05\u5409\u4fdd\u5e73\u5b89"], [2, "\u65bc\u4eca\u6b64\u666f\u6b63\u7576\u6642,\u770b\u770b\u6b32\u5410\u767e\u82b1\u9b41,\u82e5\u80fd\u9047\u5f97\u6625\u8272\u5230,\u4e00\u6d12\u6e05\u5409\u812b\u5875\u57c3"], [3, "\u52f8\u541b\u628a\u5b9a\u5fc3\u83ab\u865b,\u5929\u8a3b\u8863\u797f\u81ea\u6709\u9918,\u548c\u5408\u91cd\u91cd\u5e38\u5409\u6176,\u6642\u4f86\u7d42\u9047\u5f97\u660e\u73e0"], [4, "\u98a8\u606c\u6d6a\u975c\u53ef\u884c\u821f,\u6070\u662f\u4e2d\u79cb\u6708\u4e00\u8f2a,\u51e1\u4e8b\u4e0d\u9808\u591a\u6182\u616e,\u798f\u797f\u81ea\u6709\u6176\u5bb6\u9580"], [5, "\u53ea\u6050\u524d\u9014\u547d\u6709\u8b8a,\u52f8\u541b\u4f5c\u6025\u53ef\u5b9c\u5148,\u4e14\u5b88\u9577\u6c5f\u7121\u5927\u4e8b,\u547d\u9022\u592a\u767d\u5b88\u8eab\u908a"], [6, "\u98a8\u96f2\u81f4\u96e8\u843d\u6d0b\u6d0b,\u5929\u707d\u6642\u6c23\u5fc5\u6709\u50b7,\u547d\u5167\u6b64\u4e8b\u96e3\u548c\u5408,\u66f4\u9022\u4e00\u8db3\u51fa\u5916\u9109"], [7, "\u96f2\u958b\u6708\u51fa\u6b63\u5206\u660e,\u4e0d\u9808\u9032\u9000\u554f\u524d\u7a0b,\u5a5a\u59fb\u7686\u7531\u5929\u8a3b\u5b9a,\u548c\u5408\u6e05\u5409\u842c\u4e8b\u6210\u3000"], [8, "\u79be\u7a3b\u770b\u770b\u7d50\u6210\u5b8c,\u6b64\u4e8b\u5fc5\u5b9a\u5169\u76f8\u5168,\u56de\u5230\u5bb6\u4e2d\u5bec\u5fc3\u5750,\u59bb\u5152\u9f13\u821e\u6a02\u5718\u5713"], [9, "\u9f8d\u864e\u76f8\u96a8\u5728\u6df1\u5c71,\u541b\u723e\u4f55\u9808\u80cc\u5f8c\u770b,\u4e0d\u77e5\u6b64\u53bb\u76f8\u611b\u6109,\u4ed6\u65e5\u8207\u6211\u537b\u7121\u5e72"], [10, "\u82b1\u958b\u7d50\u5b50\u4e00\u534a\u67af,\u53ef\u60dc\u4eca\u5e74\u6c5d\u865b\u5ea6,\u6f38\u6f38\u65e5\u843d\u897f\u5c71\u53bb,\u52f8\u541b\u4e0d\u7528\u5411\u524d\u9014"], [11, "\u9748\u96de\u6f38\u6f38\u898b\u5206\u660e,\u51e1\u4e8b\u4e14\u770b\u5b50\u4e11\u5bc5,\u96f2\u958b\u6708\u51fa\u7167\u5929\u4e0b,\u90ce\u541b\u5373\u4fbf\u898b\u592a\u5e73"], [12, "\u9577\u6c5f\u98a8\u6d6a\u6f38\u6f38\u975c,\u4e8e\u4eca\u5f97\u9032\u53ef\u5b89\u5be7,\u5fc5\u6709\u8cb4\u4eba\u76f8\u6276\u52a9,\u51f6\u4e8b\u812b\u51fa\u898b\u592a\u5e73"], [13, "\u547d\u4e2d\u6b63\u9022\u7f85\u5b5b\u95dc,\u7528\u76e1\u5fc3\u6a5f\u7e3d\u672a\u4f11,\u4f5c\u798f\u554f\u795e\u96e3\u5f97\u904e,\u6070\u662f\u884c\u821f\u4e0a\u9ad8\u7058"], [14, "\u8ca1\u4e2d\u6f38\u6f38\u898b\u5206\u660e,\u82b1\u958b\u82b1\u8b1d\u7d50\u5b50\u6210,\u5bec\u5fc3\u4e14\u770b\u6708\u4e2d\u6842,\u90ce\u541b\u5373\u4fbf\u898b\u592a\u5e73"], [15, "\u516b\u5341\u539f\u4f86\u662f\u592a\u516c,\u770b\u770b\u665a\u666f\u9047\u6587\u738b,\u76ee\u4e0b\u7dca\u4e8b\u4f11\u76f8\u554f,\u52f8\u541b\u4e14\u5b88\u5f85\u904b\u901a"], [16, "\u4e0d\u9808\u4f5c\u798f\u4e0d\u9808\u6c42,\u7528\u76e1\u5fc3\u6a5f\u7e3d\u672a\u4f11,\u967d\u4e16\u4e0d\u77e5\u9670\u4e16\u4e8b,\u5b98\u6cd5\u5982\u7210\u4e0d\u81ea\u7531"], [17, "\u820a\u6068\u91cd\u91cd\u672a\u6539\u70ba,\u5bb6\u4e2d\u798d\u60a3\u4e0d\u81e8\u8eab,\u9808\u7576\u8b39\u9632\u5b9c\u4f5c\u798f,\u9f8d\u86c7\u4ea4\u6703\u5f97\u548c\u5408"], [18, "\u541b\u554f\u4e2d\u9593\u6b64\u8a00\u56e0,\u770b\u770b\u797f\u99ac\u62f1\u524d\u7a0b,\u82e5\u5f97\u8cb4\u4eba\u591a\u5f97\u5229,\u548c\u5408\u81ea\u6709\u5169\u5206\u660e"], [19, "\u5bcc\u8cb4\u7531\u547d\u5929\u8a3b\u5b9a,\u5fc3\u9ad8\u5fc5\u7136\u8aa4\u541b\u671f,\u4e0d\u7136\u4e14\u56de\u4f9d\u820a\u8def,\u96f2\u958b\u6708\u51fa\u81ea\u5206\u660e"], [20, "\u524d\u9014\u529f\u540d\u672a\u5f97\u610f,\u53ea\u6050\u547d\u5167\u6709\u4ea4\u52a0,\u5169\u5bb6\u5fc5\u5b9a\u9632\u640d\u5931,\u52f8\u541b\u4e14\u9000\u83ab\u54a8\u55df"], [21, "\u5341\u65b9\u4f5b\u6cd5\u6709\u9748\u901a,\u5927\u96e3\u798d\u60a3\u4e0d\u76f8\u540c,\u7d05\u65e5\u7576\u7a7a\u5e38\u7167\u8000,\u9084\u6709\u8cb4\u4eba\u5230\u5bb6\u5802"], [22, "\u592a\u516c\u5bb6\u696d\u516b\u5341\u6210,\u6708\u51fa\u5149\u8f1d\u56db\u6d77\u660e,\u547d\u5167\u81ea\u7136\u9022\u5927\u5409,\u8305\u5c4b\u4e2d\u9593\u767e\u4e8b\u4ea8"], [23, "\u6b32\u53bb\u9577\u6c5f\u6c34\u95ca\u832b,\u524d\u9014\u672a\u9042\u904b\u672a\u901a,\u5982\u4eca\u7d72\u7db8\u5e38\u5728\u624b,\u53ea\u6050\u9b5a\u6c34\u4e0d\u76f8\u9022"], [24, "\u6708\u51fa\u5149\u8f1d\u56db\u6d77\u660e,\u524d\u9014\u797f\u4f4d\u898b\u592a\u5e73,\u6d6e\u96f2\u6383\u9000\u7d42\u7121\u4e8b,\u53ef\u4fdd\u798d\u60a3\u4e0d\u81e8\u8eab"], [25, "\u7e3d\u662f\u524d\u9014\u83ab\u5fc3\u52de,\u6c42\u795e\u554f\u8056\u6789\u662f\u591a,\u4f46\u770b\u96de\u72ac\u65e5\u904e\u5f8c,\u4e0d\u9808\u4f5c\u798f\u4e8b\u5982\u4f55"], [26, "\u9078\u51fa\u7261\u4e39\u7b2c\u4e00\u679d,\u52f8\u541b\u6298\u53d6\u83ab\u9072\u7591,\u4e16\u9593\u82e5\u554f\u76f8\u77e5\u8655,\u842c\u4e8b\u9022\u6625\u6b63\u53ca\u6642"], [27, "\u541b\u723e\u5bec\u5fc3\u4e14\u81ea\u7531,\u9580\u5ead\u6e05\u5409\u5bb6\u7121\u6182,\u8ca1\u5bf6\u81ea\u7136\u7d42\u5409\u5229,\u51e1\u4e8b\u7121\u50b7\u4e0d\u7528\u6c42"], [28, "\u65bc\u4eca\u83ab\u4f5c\u6b64\u7576\u6642,\u864e\u843d\u5e73\u967d\u88ab\u72ac\u6b3a,\u4e16\u9593\u51e1\u4e8b\u4f55\u96e3\u5b9a,\u5343\u5c71\u842c\u6c34\u4e5f\u9072\u7591"], [29, "\u67af\u6728\u53ef\u60dc\u672a\u9022\u6625,\u5982\u4eca\u8fd4\u5728\u6697\u4e2d\u85cf,\u5bec\u5fc3\u4e14\u5b88\u98a8\u971c\u9000,\u9084\u541b\u4f9d\u820a\u4f5c\u4e7e\u5764"], [30, "\u6f38\u6f38\u770b\u6b64\u6708\u4e2d\u548c,\u904e\u5f8c\u9808\u9632\u672a\u5f97\u9ad8,\u6539\u8b8a\u984f\u8272\u524d\u9014\u53bb,\u51e1\u4e8b\u5fc5\u5b9a\u898b\u91cd\u52de"], [31, "\u7da0\u67f3\u84bc\u84bc\u6b63\u7576\u6642,\u4efb\u541b\u6b64\u53bb\u4f5c\u4e7e\u5764,\u82b1\u679c\u7d50\u5be6\u7121\u6b98\u8b1d,\u798f\u797f\u81ea\u6709\u6176\u5bb6\u9580"], [32, "\u9f8d\u864e\u76f8\u4ea4\u5728\u9580\u524d,\u6b64\u4e8b\u5fc5\u5b9a\u5169\u76f8\u9023,\u9ec3\u91d1\u5ffd\u7136\u8b8a\u6210\u9435,\u4f55\u7528\u4f5c\u798f\u554f\u795e\u4ed9"], [33, "\u6b32\u53bb\u9577\u6c5f\u6c34\u95ca\u832b,\u884c\u821f\u628a\u5b9a\u672a\u906d\u98a8,\u6236\u5167\u7528\u5fc3\u518d\u4f5c\u798f,\u770b\u770b\u9b5a\u6c34\u5f97\u76f8\u9022"], [34, "\u5371\u96aa\u9ad8\u5c71\u884c\u904e\u76e1,\u83ab\u5acc\u6b64\u8def\u6709\u91cd\u91cd,\u82e5\u898b\u862d\u6842\u6f38\u6f38\u767c,\u9577\u86c7\u53cd\u8f49\u8b8a\u6210\u9f8d"], [35, "\u6b64\u4e8b\u4f55\u9808\u7528\u5fc3\u6a5f,\u524d\u9014\u8b8a\u602a\u81ea\u7136\u77e5,\u770b\u770b\u6b64\u53bb\u5f97\u548c\u5408,\u6f38\u6f38\u812b\u51fa\u898b\u592a\u5e73"], [36, "\u798f\u5982\u6771\u6d77\u58fd\u5982\u5c71,\u541b\u723e\u4f55\u9808\u5606\u82e6\u96e3,\u547d\u5167\u81ea\u7136\u9022\u5927\u5409,\u7948\u4fdd\u5206\u660e\u81ea\u5e73\u5b89"], [37, "\u904b\u9022\u5f97\u610f\u8eab\u986f\u8b8a,\u541b\u723e\u8eab\u4e2d\u7686\u6709\u76ca,\u4e00\u5411\u524d\u9014\u7121\u96e3\u4e8b,\u6c7a\u610f\u4e4b\u4e2d\u4fdd\u6e05\u5409"], [38, "\u540d\u986f\u6709\u610f\u5728\u4e2d\u592e,\u4e0d\u9808\u7948\u79b1\u5fc3\u81ea\u5b89,\u770b\u770b\u65e9\u665a\u65e5\u904e\u5f8c,\u5373\u6642\u5f97\u610f\u5728\u5176\u9593"], [39, "\u610f\u4e2d\u82e5\u554f\u795e\u4ed9\u8def,\u52f8\u723e\u4e14\u9000\u671b\u9ad8\u6a13,\u5bec\u5fc3\u4e14\u5b88\u5bec\u5fc3\u5750,\u5fc5\u7136\u9047\u5f97\u8cb4\u4eba\u6276"], [40, "\u5e73\u751f\u5bcc\u8cb4\u6210\u797f\u4f4d,\u541b\u5bb6\u9580\u6236\u5b9a\u5149\u8f1d,\u6b64\u4e2d\u5fc5\u5b9a\u7121\u640d\u5931,\u592b\u59bb\u767e\u6b72\u559c\u76f8\u96a8"], [41, "\u4eca\u884c\u5230\u6b64\u5be6\u96e3\u63a8,\u6b4c\u6b4c\u66a2\u98f2\u81ea\u5f98\u5f8a,\u96de\u72ac\u76f8\u805e\u6d88\u606f\u8fd1,\u5a5a\u59fb\u5919\u4e16\u7d50\u6210\u96d9"], [42, "\u4e00\u91cd\u6c5f\u6c34\u4e00\u91cd\u5c71,\u8ab0\u77e5\u6b64\u53bb\u8def\u53c8\u96e3,\u4efb\u4ed6\u6539\u6c42\u7d42\u4e0d\u904e,\u662f\u975e\u7d42\u4e45\u672a\u5f97\u5b89"], [43, "\u4e00\u5e74\u4f5c\u4e8b\u6025\u5982\u98db,\u541b\u723e\u5bec\u5fc3\u83ab\u9072\u7591,\u8cb4\u4eba\u9084\u5728\u5343\u91cc\u5916,\u97f3\u4fe1\u6708\u4e2d\u6f38\u6f38\u77e5"], [44, "\u5ba2\u5230\u524d\u9014\u591a\u5f97\u5229,\u541b\u723e\u4f55\u6545\u5169\u76f8\u7591,\u96d6\u662f\u4e2d\u9593\u9632\u9032\u9000,\u6708\u51fa\u5149\u8f1d\u5f97\u904b\u6642"], [45, "\u82b1\u958b\u4eca\u5df2\u7d50\u6210\u679c,\u5bcc\u8cb4\u69ae\u83ef\u7d42\u5230\u8001,\u541b\u5b50\u5c0f\u4eba\u76f8\u6703\u5408,\u842c\u4e8b\u6e05\u5409\u83ab\u7169\u60f1"], [46, "\u529f\u540d\u5f97\u610f\u8207\u541b\u986f,\u524d\u9014\u5bcc\u8cb4\u559c\u5b89\u7136,\u82e5\u9047\u4e00\u8f2a\u660e\u6708\u7167,\u5341\u4e94\u5718\u5713\u5149\u6eff\u5929"], [47, "\u541b\u723e\u4f55\u9808\u554f\u8056\u8de1,\u81ea\u5df1\u5fc3\u4e2d\u7686\u6709\u76ca,\u65bc\u4eca\u4e14\u770b\u6708\u4e2d\u65ec,\u51f6\u4e8b\u812b\u51fa\u5316\u6210\u5409"], [48, "\u967d\u4e16\u4f5c\u4e8b\u672a\u548c\u540c,\u96f2\u906e\u6708\u8272\u6b63\u6726\u6727,\u5fc3\u4e2d\u610f\u6b32\u524d\u9014\u53bb,\u53ea\u6050\u547d\u5167\u904b\u672a\u901a"], [49, "\u8a00\u8a9e\u96d6\u591a\u4e0d\u53ef\u5f9e,\u98a8\u96f2\u975c\u8655\u672a\u884c\u9f8d,\u6697\u4e2d\u7d42\u5f97\u660e\u6d88\u606f,\u541b\u723e\u4f55\u9808\u554f\u91cd\u91cd"], [50, "\u4f5b\u524d\u767c\u8a93\u7121\u7570\u5fc3,\u4e14\u770b\u524d\u9014\u5f97\u597d\u97f3,\u6b64\u7269\u539f\u4f86\u672c\u662f\u9435,\u4e5f\u80fd\u8b8a\u5316\u5f97\u6210\u91d1"], [51, "\u6771\u897f\u5357\u5317\u4e0d\u582a\u884c,\u524d\u9014\u6b64\u4e8b\u6b63\u53ef\u7576,\u52f8\u541b\u628a\u5b9a\u83ab\u7169\u60f1,\u5bb6\u9580\u81ea\u6709\u4fdd\u5b89\u5eb7"], [52, "\u529f\u540d\u4e8b\u696d\u672c\u7531\u5929,\u4e0d\u9808\u639b\u5ff5\u610f\u61f8\u61f8,\u82e5\u554f\u4e2d\u9593\u9072\u8207\u901f,\u98a8\u96f2\u969b\u6703\u5728\u773c\u524d"], [53, "\u770b\u541b\u4f86\u554f\u5fc3\u4e2d\u4e8b,\u7a4d\u5584\u4e4b\u5bb6\u6176\u6709\u9918,\u904b\u4ea8\u8ca1\u5b50\u96d9\u96d9\u81f3,\u6307\u65e5\u559c\u6c23\u6ea2\u9580\u95ad"], [54, "\u5b64\u71c8\u5bc2\u5bc2\u591c\u6c89\u6c89,\u842c\u4e8b\u6e05\u5409\u842c\u4e8b\u6210,\u82e5\u9022\u9670\u4e2d\u6709\u5584\u679c,\u71d2\u5f97\u597d\u9999\u9054\u795e\u660e"], [55, "\u9808\u77e5\u9032\u9000\u7e3d\u8a00\u865b,\u770b\u770b\u767c\u6697\u672a\u5fc5\u5168,\u73e0\u7389\u6df1\u85cf\u9084\u672a\u8b8a,\u5fc3\u4e2d\u4f46\u5f97\u6789\u5f92\u7136"], [56, "\u75c5\u4e2d\u82e5\u5f97\u82e6\u5fc3\u52de,\u5230\u5e95\u5b8c\u5168\u7e3d\u672a\u906d,\u53bb\u5f8c\u4e0d\u9808\u56de\u982d\u554f,\u5fc3\u4e2d\u4e8b\u52d9\u76e1\u6d88\u78e8"], [57, "\u52f8\u541b\u628a\u5b9a\u5fc3\u83ab\u865b,\u524d\u9014\u6e05\u5409\u5f97\u904b\u6642,\u5230\u5e95\u4e2d\u9593\u7121\u5927\u4e8b,\u53c8\u9047\u795e\u4ed9\u5b88\u5b89\u5c45"], [58, "\u86c7\u8eab\u610f\u6b32\u8b8a\u6210\u9f8d,\u53ea\u6050\u547d\u5167\u904b\u672a\u901a,\u4e45\u75c5\u4e14\u4f5c\u5bec\u5fc3\u5750,\u8a00\u8a9e\u96d6\u591a\u4e0d\u53ef\u5f9e"], [59, "\u6709\u5fc3\u4f5c\u798f\u83ab\u9072\u7591,\u6c42\u540d\u6e05\u5409\u6b63\u7576\u6642,\u6b64\u4e8b\u5fc5\u80fd\u6210\u6703\u5408,\u8ca1\u5bf6\u81ea\u7136\u559c\u76f8\u96a8"], [60, "\u6708\u51fa\u5149\u8f1d\u672c\u6e05\u5409,\u6d6e\u96f2\u7e3d\u662f\u853d\u9670\u8272,\u6236\u5167\u7528\u5fc3\u518d\u4f5c\u798f,\u7576\u5b98\u5206\u7406\u4fbf\u6709\u76ca"], [61, "\u7c64\u982d\u767e\u4e8b\u826f\u3000,\u6dfb\u6cb9\u5927\u5409\u660c\u3000,\u842c\u822c\u7686\u5982\u610f\u3000\u3000,\u5bcc\u8cb4\u798f\u58fd\u9577"], [62, "\u5f1f\u5b50\u8654\u8aa0\u5230\u6b64\u6c42,\u795e\u9748\u611f\u61c9\u5e7e\u5343\u79cb,\u62bd\u5f97\u6b64\u7c64\u767e\u4e8b\u5409,\u9700\u7576\u4f86\u6dfb\u4f5b\u524d\u6cb9"], [63, "\u4f86\u610f\u6b32\u6c42\u5929\u4e0a\u798f,\u8aa0\u5fc3\u9808\u9ede\u4f5b\u524d\u71c8,\u540d\u5229\u5169\u5168\u7686\u5927\u5409,\u5e73\u5b89\u916c\u8b1d\u6cb9\u4e09\u65a4"], [64, "\u4efb\u7948\u6240\u6c42\u7686\u5927\u5409,\u4e00\u5411\u524d\u9014\u632f\u8f1d\u9a30,\u6c42\u5f97\u7c64\u738b\u842c\u4e8b\u6210,\u6dfb\u6cb9\u4e09\u65a4\u9ede\u4f5b\u71c8"]]


def GetCard():
    return futune_lots

def GetCardById(id) -> list:
    if id > 64 or id < 1:
        return [0,""]
    return futune_lots[id-1]

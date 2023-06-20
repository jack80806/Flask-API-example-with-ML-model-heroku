from fastapi import FastAPI  # 匯入 FastAPI 框架
from pydantic import BaseModel  # 用於建立資料模型
from typing import Optional  # 型別註釋用於建立可選型別
from fastapi.encoders import jsonable_encoder  # 用於將 Python 資料結構轉換為 JSON
from fastapi.responses import JSONResponse  # 用於建立 JSON 回應
import requests  # 用於建立 HTTP 請求

app = FastAPI()  # 建立 FastAPI 應用實例

# 定義全局變量
flagForSymptoms: Optional[int] = 0
flagForBasicInfo: Optional[int] = 0


urlForChange = "https://for-api-32f276cf322d.herokuapp.com/changeFlag"  # API 的 URL

# 定義Flag資料模型
class FlagModel(BaseModel):
    target: str
    val: int

# 定義端點，該端點負責更改旗標值
@app.post("/changeFlag")
def post_for_change_flag(flag: FlagModel):
    # 透過全局變量的方式來改變旗標值
    global flagForSymptoms
    global flagForBasicInfo


    # 根據目標旗標的名稱來改變其值，然後返回"OK"
    if flag.target == "flagForSymptoms":
        flagForSymptoms = flag.val
        return "OK"
    elif flag.target == "flagForBasicInfo":
        flagForBasicInfo = flag.val
        return "OK"
    

    return "fail"  # 如果無法匹配任何旗標名稱，則返回"fail"

# 定義一個全新的資料模型來儲存所有的旗標
class AllFlagModel(BaseModel):
    flagForSymptoms: int
    flagForBasicInfo: int


# 定義一個新的端點，該端點會一次更改所有旗標的值
@app.post("/changeAllFlag")
def post_for_change_All_flag(flag: AllFlagModel):
    # 透過全局變量的方式來改變旗標值
    global flagForSymptoms
    global flagForBasicInfo

    flagForSymptoms = flag.flagForSymptoms
    flagForBasicInfo = flag.flagForBasicInfo


    return "OK"  # 更改成功後返回"OK"

# 這個端點將所有的旗標以 JSON 格式返回
@app.get("/getFlag")
def get_for_flag():
    return jsonable_encoder(
        {
            "flagForSymptoms": flagForSymptoms,
            "flagForBasicInfo": flagForBasicInfo,
            "flagForRecords": flagForRecords,
            "flagForClinic": flagForClinic,
        }
    )

# 這個端點用於取得基本資訊
@app.get("/basicInfo")
def get_for_basic_info():
    userid = "Ucb952f1a00be8f43598a7ac8f449831a"  # 使用者 ID
    flag = flagForBasicInfo  # 獲取旗標值

    # 準備資料
    data = {"userid": userid}

    # 發送 POST 請求
    response = requests.post(
        "https://us-central1-fortesting-c54ba.cloudfunctions.net/post/accessbasic",
        data=data,
    )

    # 從回應中提取資料
    if response.status_code == 200:
        user_data = response.json()
    else:
        user_data = {}

    # 準備最終結果
    result = {"flag": flag, "userID": userid, "result": user_data["result"]}

    return jsonable_encoder(result)  # 將結果以 JSON 格式返回

# 定義資料模型
class SymptomsModel(BaseModel):
    userID: str

# 這個端點用於取得症狀資訊
@app.post("/symptoms")
def post_for_symptoms(symptoms: SymptomsModel):
    userid = symptoms.userID  # 使用者 ID
    flag = flagForSymptoms  # 獲取旗標值

    # 準備資料
    data = {"userid": userid}

    # 如果 flagForSymptoms 為 1，則發送 POST 請求並取得症狀資訊，否則返回{"flag": 0, "result": {"symptoms": ""}}
    # 該部分的處理過程包括發送 POST 請求、提取回應資料、準備最終結果、以及改變旗標值等步驟

# 定義資料模型
class ClinicModel(BaseModel):
    userID: str

# 這個端點用於取得診所資訊
@app.post("/forClinic")
def post_for_clinic(clinic: ClinicModel):
    userid = clinic.userID  # 使用者 ID

    # 準備資料
    data = {"userid": userid}

    # 發送 POST 請求並取得診所資訊，該部分的處理過程包括發送 POST 請求、提取回應資料、準備最終結果、以及改變旗標值等步驟

# 定義資料模型
class RecordsModel(BaseModel):
    userID: str

# 這個端點用於取得紀錄
@app.post("/records")
def post_for_records(records: RecordsModel):
    userid = records.userID  # 使用者 ID

    # 準備資料
    data = {"userid": userid}

    # 發送 POST 請求並取得紀錄，該部分的處理過程包括發送 POST 請求、提取回應資料、準備最終結果、以及改變旗標值等步驟

# 定義資料模型
class NextStepModel(BaseModel):
    nextStep: str

# 這個端點用於發布下一步的資訊
@app.post("/nextStep")
def post_next_step(next_step: NextStepModel):
    return "OK"  # 返回"OK"

# 這個端點用於取得偽造的基本資訊
@app.get("/FakeBasicInfo")
def get_for_basic_info():
    return jsonable_encoder(
        {
            "flag": flagForBasicInfo,
            "result": {
                "id": "Ace",
                "familyHistory": "心臟病, 高血壓, 糖尿病",
                "weight": "60",
                "age": "18",
                "height": "180",
            },
        }
    )

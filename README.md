# 資料夾路徑
```
 |-run.py
 |
 |-createSA.py
 |
 |-instance             #存放金鑰
 |
 |-app
 |    |
 |    |-models          #操控資料庫
 |    |
 |    |-static          #存放css, img, js
 |    |       |
 |    |       |-css
 |    |       |    |
 |    |       |    |-test
 |    |       |
 |    |       |-img
 |    |       |
 |    |       |-js
 |    |           |
 |    |           |-test
 |    |
 |    |-templates       #存放html
 |    |
 |    |-views           #存放API
```

<br>
<br>

# 文件說明


## run.py
伺服器主要執行檔
## createSA.py
建立SA帳號
## dao.py
Data Access Object(再不看R)
## hash.py
加密密碼


<br>
<br>

# API 1 - USER Detect Repeated
### POST
#### 在一般使用者註冊時偵測帳號是否重複
#### path : /test/USER/detect_repeated (account)
>tip : JavaScript can use onkeyup
```
request:

{
	userName: "" (max length 20)
}

response:

{
	rspCode: ""		200:沒有重複 | 300:method使用錯誤 | 400: 資料庫錯誤 | 401:帳號格式不符 | 402:偵測到重複帳號
}
```

<br>

# API 2 - USER Register
### POST
#### 供一般使用者註冊
#### path : /test/USER/register (account)
```
request:

{
	userName: "",		(max length 20)
	name: "",			(max length 20)
	userPassword: "",	(max length 30)
	userMail: "",		(max length 50)
	userPhone: "",		(max length 20)
	userGender: "",		0:male | 1:female | 2:other
	userBirthday: ""
}

response:

{
	rspCode: ""		200:success | 300:method使用錯誤 | 400:資料庫錯誤 | 401:名稱長度不符 | 402:帳號格式不符 | 403:密碼格式不符 | 404:電子郵件長度不符 | 405:電子郵件格式不符 | 406:手機號碼格式不符 | 407:性別異常 | 408:生日格式不符 | 409:未來人錯誤 | 410:帳號重複 | 411:電子郵件重複
}
```

<br>

# API 3 - USER Login
### POST
#### 供一般使用者登入
#### path : /test/USER/login
```
request:

{
	type: "",			0:no login | 1:USER | 2:AS | 3:AA | 4:AU | 5:AG | 6:GM | 7:SA
	userName: "",			(max length 20)
	userPassword: ""	(max length 30)
}

response:

{
	rspCode: "",		200:登入成功 | 300:method使用錯誤 | 400:資料庫錯誤 | 401:登入失敗，沒有該帳號 | 402:登入失敗，密碼錯誤
}
```

<br>

# API 4 - Logout
### GET
#### 供所有使用者登出
#### path : /test/logout
```
request:

{
	null
}

response:

{
	rspCode: ""		200:登出成功 | 400:登出失敗
}
```

<br>

# API 5 - USER forgot Password
### POST 
#### 供一般使用者申請重設密碼信
#### path : /test/USER/forgot_password
```
request:

{
	userMail: ""	(max length 50)
}

response:

{
	rspCode: ""		200:重置信寄送成功 | 300:method使用錯誤 | 400:資料庫錯誤 | 401:電子郵件長度不符 | 402:電子郵件格式不符 | 403:電子郵件輸入錯誤，沒有找到對應的電子郵件 | 404:重置信寄送失敗
}
```

<br>

# API 6 - USER Reset Password
### POST
#### 在驗證token後一般使用者能夠重設密碼
#### path : /test/USER/reset_password/\<token\>
>tip:需要將網址中最後段的token擷取下來並放在API路徑中
```
request:

{
	userPassword: ""	(max length 30)
}

response:

{
	rspCode: ""		200:重設密碼成功 | 300:method使用錯誤 | 400:資料庫錯誤 | 401:token驗證失敗 | 402:密碼格式不符
}
```

<br>

# API 7 - Admin Detect Repeated
### POST
#### 新增管理員時避免帳號重複
#### path : /test/Admin/detect_repeated
```
request:

{
	adminName: ""		(max length 20)
}

response:

{
	rspCode: ""		200:沒有重複 | 300:method使用錯誤 | 400: 資料庫錯誤 | 401:帳號格式不符 | 402:偵測到重複帳號
}
```

<br>

# API 8 - Create Admin
### POST
#### SA新增管理員
#### path : /test/create/Admin (HRManage)
```
request:

{
	adminType: ""			2:AS | 3:AA | 4:AU | 5:AG
	adminName: ""		 	(max length 20)
	adminPassword: ""		(max length 30)
}

response:

{
	rspCode: ""			200:管理員新增成功 | 300:method使用錯誤 | 400:資料庫錯誤 | 401:adminType異常 | 402:帳號格式不符 | 403:密碼格式不符 | 404:帳號重複
}
```

<br>

# API 9 - Delete Admin
### POST
#### SA刪除管理員
#### path : /test/delete/Admin (HRManage)
>我想讓SA輸入一次密碼再進行刪除的動作，第一次點擊刪除(SAPassword留空)顯示輸入密碼，輸入一次後就不必再輸入
```
request:

{
	adminID: ""			
	SAID: ""			(之後有登入就不需要)
}

response:

{
	rspCode: ""			200:刪除成功 | 300:method使用錯誤 | 400:資料庫錯誤 | 401:adminID不在資料庫中，前端可能遭到竄改 | 402:該帳號目前不是admin | 403:尚未輸入第一次密碼
}
```

<br>

# API 10 - Admin List
### GET
#### 取得現有Admin列表
#### path : /test/Admin_list
```
request:

{
	NULL
}

response:

{
	rspCode: "",	200:成功
	AdminList: [
		{
			adminID: ""
			adminType: "",		2:AS | 3:AA | 4:AU | 5:AG
			adminName: "",
			adminPhone: "",
			adminMail: ""
		}
	]
}
```

<br>

# API 11 - GM Register
### POST
#### 路人能夠申請註冊GM資格，並寄發驗證信
#### path : /test/GM/register
```
request:

{
	GMName: "",		(max length 20)
	GMPassword: "",	(max length 30)
	GMMail: "",		(max length 50)
	GMPhone: ""
}

response:

{
	rspCode: ""		200:電子郵件已被輸入，驗證信寄送成功 | 201:電子郵件已申請過，驗證信再次寄出 | 202:帳號申請成功，驗證信已寄出 | 300:method使用錯誤 | 400:資料庫錯誤 | 401:帳號格式不符 | 402:密碼格式不符 | 403:電子郵件長度不符 | 404:電子郵件格式不符 | 405:手機號碼格式不符 | 406:帳號與他人重複 | 407.408.410:驗證信寄送失敗 | 409:電子郵件與他人重複
}
```

<br>

# API 12 - Approve GM
### POST
#### SA及AG能夠同意GM註冊申請
#### path : /test/approveGM
```
request:

{
	GMID: ""
}

response:

{
	rspCode: ""		200:同意GM申請成功 | 300:method使用錯誤 | 400:資料庫錯誤 | 401:該帳號並非待審核GM，前端可能遭竄改
}
```

<br>

# API 13 - Reject GM
### POST
#### SA及AG能夠拒絕GM註冊申請
#### path : /test/rejectGM
```
request:

{
	GMID: ""
}

response:

{
	rspCode: ""		200:拒絕GM申請成功 | 300:method使用錯誤 | 400:資料庫錯誤 | 401:該帳號並非待審核GM，前端可能遭竄改
}
```

<br>

# API 14 - Admin Login
### POST
#### 所有管理員登入
#### path : /Admin/login
```
request:

{
	adminName: ""
	adminPassword: ""
}

response:

{
	rspCode: ""		200:登入成功 | 300:method使用錯誤 | 400:資料庫錯誤 | 401:登入失敗，沒有該帳號 | 402:登入失敗，密碼輸入錯誤
}
```

<br>


# API 15 - Load GM Mail
### POST
#### SA及AG能夠輸入GM的EMail
#### path : /test/load_GM_mail
```
request:

{
	GMMail: ""		(max length 50)
}

response:

{
	rspCode: ""		200:email輸入成功 | 300:method使用錯誤 | 400:資料庫錯誤 | 401: email格式不符 | 402:email與他人重複
}
```

<br>

# API 16 - GM Apply List
### GET
#### 取得GM申請列表
#### path : /GM_apply_list
```
request:

{
	NULL
}

response:

{
	rspCode: "",	200:成功
	applyList: [
		{
			adminID: "",
			adminName: "",
			adminPhone: "",
			adminMail: ""
		}
	]
}
```

<br>

# API 17 - GM List
### GET
#### 取得現有GM列表
#### path : /GM_list
```
request:

{
	NULL
}

response:

{
	rspCode: "",	200:成功
	GMList: [
		{
			adminID: "",
			adminName: "",
			adminPhone: "",
			adminMail: ""
		}
	]
}
```

<br>

# API 18 - Delete GM
### POST
#### SA及AG能夠刪除GM
#### path : /test/delete/GM
>當rspCode為403就跳出視窗讓管理員輸入密碼，再來就能夠連續刪除
```
request:

{
	GMID: "",
	adminID: "",			(之後有登入就不用)
}

response:

{
	rspCode: ""		200:刪除成功 | 300:method使用錯誤 | 400:資料庫錯誤 | 401:GMID不在資料庫中，前端可能遭到竄改 | 402:ID錯誤，此ID可能不是GM | 403:尚未輸入第一次密碼
}
```

<br>

# API 18 - Admin forgot Password
### POST 
#### 供管理員申請重設密碼信
#### path : /test/Admin/forgot_password
```
request:

{
	adminMail: ""	(max length 50)
}

response:

{
	rspCode: ""		200:重置信寄送成功 | 300:method使用錯誤 | 400:資料庫錯誤 | 401:電子郵件長度不符 | 402:電子郵件格式不符 | 403:電子郵件輸入錯誤，沒有找到對應的電子郵件 | 404:重置信寄送失敗
}
```

<br>

# API 19 - Admin Reset Password
### POST
#### 在驗證token後一般使用者能夠重設密碼
#### path : /test/Admin/reset_password/\<token\>
>tip:需要將網址中最後段的token擷取下來並放在API路徑中
```
request:

{
	adminPassword: ""	(max length 30)
}

response:

{
	rspCode: ""		200:重設密碼成功 | 300:method使用錯誤 | 400:資料庫錯誤 | 401:token驗證失敗 | 402:密碼格式不符
}
```

# API 20 - GM forgot Password
### POST 
#### 供GM申請重設密碼信
#### path : /test/USER/forgot_password
```
request:

{
	GMMail: ""	(max length 50)
}

response:

{
	rspCode: ""		200:重置信寄送成功 | 300:method使用錯誤 | 400:資料庫錯誤 | 401:電子郵件長度不符 | 402:電子郵件格式不符 | 403:電子郵件輸入錯誤，沒有找到對應的電子郵件 | 404:重置信寄送失敗 | 405:該帳號不是GM
}
```

<br>

# API 21 - GM Reset Password
### POST
#### 在驗證token後一般使用者能夠重設密碼
#### path : /test/GM/reset_password/\<token\>
>tip:需要將網址中最後段的token擷取下來並放在API路徑中
```
request:

{
	GMPassword: ""	(max length 30)
}

response:

{
	rspCode: ""		200:重設密碼成功 | 300:method使用錯誤 | 400:資料庫錯誤 | 401:token驗證失敗 | 402:密碼格式不符
}
```

<br>

# API 22 - Delete Admin Check Password
### POST
#### 刪除管理員前驗證密碼
#### path : /test/delete/Admin/check_password
```
request:

{
	SAID: ""			(之後有登入就不用)
	SAPassword: ""		(max length 30)
}

response:

{
	rspCode: ""		200:驗證密碼成功 | 300:method | 400:資料庫錯誤 | 401:密碼輸入錯誤
}
```

<br>

# API 22 - Delete Admin Check Password
### POST
#### 刪除管理員前驗證密碼
#### path : /test/delete/Admin/check_password
```
request:

{
	adminID: ""				(之後有登入就不用)
	adminPassword: ""		(max length 30)
}

response:

{
	rspCode: ""		200:驗證密碼成功 | 300:method | 400:資料庫錯誤 | 401:密碼輸入錯誤
}
```

<br>

>setting部分的userID之後都會由後端抓，測試時在json丟進來即可

<br>

# API 23 - Setting UserInfo
### POST
#### 設定使用者介紹內容
#### path : /test/setting/userInfo
```
request:

{
	userID: "",
	userInfo: ""
}

response:

{
	rspCode: ""		200:使用者介紹修改成功 | 300:method使用錯誤 | 400:資料庫錯誤 | 401:介紹並未做更動 | 402:非法字元
}
```

<br>

# API 24 - Setting Name
### POST
#### 設定名稱
#### path : /test/setting/name
```
request:

{
	userID: "",
	name: ""		(max length 20)
}

response:

{
	rspCode: ""		200:名稱修改成功 | 300:method使用錯誤 | 400:資料庫錯誤 | 401:名稱長度不符 | 402:名稱並未做更動 | 403:非法字元
}
```

<br>

# API 25 - Setting UserName
### POST
#### 設定使用者名稱
#### path : /test/setting/userName
```
request:

{
	userID: "",
	userName: ""
}

response:

{
	rspCode: ""		200:使用者名稱修改成功 | 300:method使用錯誤 | 400:資料庫錯誤 | 401:使用者名稱格式不符 | 402:使用者名稱並未做更動 | 403:使用者名稱與他人重複 | 404:非法字元
}
```

<br>

# API 26 - Setting UserPassword
### POST
#### 設定密碼
#### path : /test/setting/uesrPassword
```
request:

{
	userID: "",
	userPassword: "",		(max length 30)
	userOldPassword: ""		(max length 30)
}

response:

{
	rspCode: ""		200:密碼修改成功 | 300:method使用錯誤 | 400:資料庫錯誤 | 401:舊密碼錯誤 | 402:密碼並未做更動 | 403:密碼格式不符 | 404:非法字元
}
```

<br>

# API 27 - Setting UserMail
### POST
#### 設定電子郵件
#### path : /test/setting/userMail
```
request:

{
	userID: "",
	userMail: ""
}

response:

{
	rspCode: ""		200:電子郵件修改成功 | 300:method使用錯誤 | 400:資料庫錯誤 | 401:電子郵件長度不符 | 402:電子郵件格式不符 | 403:電子郵件並未做更動 | 404:電子郵件已被使用 | 405:非法字元
}
```

<br>

# API 28 - Setting UserPhone
### POST
#### 設定手機號碼
#### path : /test/setting/userPhone
```
request:

{
	userID: "",
	userPhone: ""
}

response:

{
	rspCode: ""		200:手機號碼修改成功 | 300:method使用錯誤 | 400:資料庫錯誤 | 401:手機號碼格式不符 | 402:手機號碼並未做更動 | 403:非法字元
}
```

<br>

# API 29 - Setting UserGender
### POST
#### 設定性別
#### path : /test/setting/userGender
```
request:

{
	userID: "",
	userGender: ""
}

response:

{
	rspCode: ""		200:性別修改成功 | 300:method使用錯誤 | 400:資料庫錯誤 | 401:性別異常 | 402:性別並未做更動 | 403:非法字元
}
```

<br>

# API 30 - Setting UserBirthday
### POST
#### 設定生日
#### path : /test/setting/userBirthday
```
request:

{
	userID: "",
	userBirthday: ""
}

response:

{
	rspCode: ""		200:生日修改成功 | 300:method使用錯誤 | 400:資料庫錯誤 | 401:生日格式不符 | 402:未來人錯誤 | 403:生日並未做更動 | 404:非法字元
}
```

<br>

# API 31 - Setting Propic
### POST
#### 設定個人照片
#### path : /test/setting/propic
>tip: form記得幫我多傳一個userID噢
```
request:

{
	propic: "",		(照片)
	userID: ""
}

response:

{
	目前應該都是直接跳轉回設定頁面
}
```

<br>

# API 32 - Profile Output
### POST
#### 顯示個人資料
#### path : /test/output
>propic放在 /static/img/propic/userID.jpg
```
request:

{
	userID: ""
}

response:

{
	rspCode: "",	200:資料成功取得 | 400:資料庫錯誤 | 300:method使用錯誤
	userID: "",
	name: "",
	userGender: "",
	userAge: "",
	userInfo: ""
}
```

<br>

# API 33 - Output SR Task Record
### POST
#### 取得SR歷史的任務
#### path : /test/SR/output/record
```
request:

{
	userID: ""
}

response:

{
	taskRecord: [
		{
			taskID: "",
			taskName: "",
			taskContent: "",
			taskPoint: "",
			taskLocation: "",
			taskStartTime: "",
			taskEndTime: "",
			taskStatus: "",
			taskSP: "",			(name需要ID再跟我說)
			taskSR: ""			(name需要ID再跟我說)
			SPScore, ""
			SPComment: "",
			SRScore, ""
			SRComment: "",
		}
	]
}
```

<br>

# API 34 - Output SP Task Passed
### POST
#### 取得SP已通過的任務
#### path : /test/SP/output/passed
```
request:

{
	userID: ""
}

response:

{
	taskRecord: [
		{
			taskID: "",
			taskName: "",
			taskContent: "",
			taskPoint: "",
			taskLocation: "",
			taskStartTime: "",
			taskEndTime: "",
			taskStatus: "",
			taskSP: "",			(name需要ID再跟我說)
			taskSR: ""			(name需要ID再跟我說)
		}
	]
}
```

<br>

# API 35 - Output SP Task Checking
### POST
#### 取得SP審核中的任務
#### path : /test/SP/output/Checking
```
request:

{
	userID: ""
}

response:

{
	taskRecord: [
		{
			taskID: "",
			taskName: "",
			taskContent: "",
			taskPoint: "",
			taskLocation: "",
			taskStartTime: "",
			taskEndTime: "",
			taskStatus: "",
			taskSP: "",			(name需要ID再跟我說)
			taskSR: ""			(name需要ID再跟我說)
		}
	]
}
```

<br>

# API 36 - Output SP Task Refused
### POST
#### 取得SP遭拒絕的任務
#### path : /test/SR/output/refused
```
request:

{
	userID: ""
}

response:

{
	taskRecord: [
		{
			taskID: "",
			taskName: "",
			taskContent: "",
			taskPoint: "",
			taskLocation: "",
			taskStartTime: "",
			taskEndTime: "",
			taskStatus: "",
			taskSP: "",			(name需要ID再跟我說)
			taskSR: ""			(name需要ID再跟我說)
		}
	]
}
```

<br>

# API 37 - Output SP Task Record
### POST
#### 取得SP歷史的任務
#### path : /test/SR/output/record
```
request:

{
	userID: ""
}

response:

{
	taskRecord: [
		{
			taskID: "",
			taskName: "",
			taskContent: "",
			taskPoint: "",
			taskLocation: "",
			taskStartTime: "",
			taskEndTime: "",
			taskStatus: "",
			taskSP: "",			(name需要ID再跟我說)
			taskSR: ""			(name需要ID再跟我說)
			SPScore, ""
			SPComment: "",
			SRScore, ""
			SRComment: "",
		}
	]
}
```

<br>

# API 38 - Output Profile Task
### POST
#### 取得個人頁面已發任務
#### path : /test/output/task
```
request:

{
	userID: ""
}

response:

{
	taskRecord: [
		{
			taskID: "",
			taskName: "",
			taskPoint: "",
			taskStartTime: "",
			taskEndTime: "",
			taskStatus: "",
		}
	]
}
```

<br>

# API 
### 
#### 
#### path : 
```
request:

{

}

response:

{
	
}
```

<br>

# Tom

理論上存在txt的沒有字數限制
1. 網站介紹存在/static/uploadFile/webIntro.txt
2. 最新消息圖片存在/static/uploadFile/newsImage/number.jpg
3. 最新消息內文存在/static/uploadFile/newsContent/number.txt

# 1.網站介紹上傳
### POST
### 上傳網站介紹
### path:/test/upload_web_intro

```
request:

{
	intro: ""		(存在txt)
}

response:

{
	rspCode: ""200 : OK |300 : methods wrong | 400 : 寫入失敗
}
```

# 2.網站介紹顯示
### GET
### 回傳網站介紹
### path:/test/output_webIntro

```
request:

{
	NULL
}

response:

{
	rspCode:"": 200 : OK |300 : methods wrong | 400:txt開啟失敗
	webIntro:""(傳網站介紹出來)
}
```

# 3.最新消息上傳
### POST
### 上傳title,img,content
### path:test/upload_news
>用form
```
request:

{
都不可為空
	title:""		(30個字以內)content
	file:""			(只能是jpg,jpeg,png)
	content:""		(傳送字串，會以txt儲存)
}

response
{
	rspCOde:""		200 : OK |300 : methods wrong | 400:title,file,content有空| 401:圖片檔名有問題| 402:圖片上傳錯誤| 403:內文上傳錯誤| 404:標題上傳錯誤| 405:title太長
}
```

# 4.最新資訊圖片顯示
### GET
### 傳最新資訊的圖片檔名
### path:/test/output_news_image/<number>
```
request:

{
	NULL
}
response

{
	rspCode: ""		200 : OK |300 : methods wrong | 400:未知 | 401:這個number沒東西
	img: ""			(圖片檔名)
}
```

# 5.最新資訊內文顯示
### GET
### 傳最新資訊的內文
### path:/test/output_news_content/<number>
```
request:

{
	NULL
}
```response:
{
	rspCode: ""		200 : OK |300 : methods wrong | 400:未知 
	content: ""		(圖片檔名)
}
```

# 6.最新資訊標題顯示
### GET
### 傳最新資訊的內文
### path:/test/output_news_title/<number>
```
request:

{
	NULL
}
response:

{
	rspCode: ""		200 : OK |300 : methods wrong | 400:未知 
	title: ""		(標題)
}
```

# 7.編輯最新消息
### POST
### 編輯網址中指定的news
### path:test/edit_news/<number>
>用form
```
request:

{
	title: ""		(小於30個字)
	content: ""		(傳送字串，會以txt儲存)
	file: ""		(jpg,png,jpeg)
}

response:

{
	rspCode: ""		200 : OK |300 : methods wrong | 400:圖片檔名錯誤 | 401:圖片更新失敗or不存在此news | 402:標題更新失敗or不存在此news | 403:內文更新失敗or不存在此news | 404:title太長 
}
```
# 8.刪除最新消息
### POST
### 刪除網址中指定的news
### path:/test/delete_news/<number>

```
request:

{
	NULL
}
response:

{
	rspCode: ""		200 : OK |300 : methods wrong | 400:title刪除失敗or不存在此news | 401:圖片不存在 | 402:圖片刪除失敗 | 403:內文刪除失敗
}
```
<br>

# 9.顯示可用的news number
### GET
### 傳可用的number和其中的最大值
### path:test/useful_numbers

``` 
request:

{
	NULL
}

response:

{
	rspCode: ""			200 : OK |300 : methods wrong | 400讀取失敗
	numberList: "" 		(可用的numbers)
	max: ""				可用的numbers中最大的
}
```

# 下面是apply的部分

申請條件pdf在app\static\uploadFile\apply_condition.pdf
申請對象txt在app\static\uploadFile\group_name.txt

# 10.更新申請對象
### POST
### 更新申請對象
### path:test/update_apply_group

```
request:

{
	groupName: ""	(對象名稱)(txt)
}
response:

{
	rspCode: ""		200 : OK |300 : methods wrong | 400(寫入失敗)
}
```

# 11.顯示申請對象
### GET
### 傳現在的申請對象是什麼
### path:test/output_apply_group

```
request:

{
	NULL
}
response:

{
	rspCode:"" 200 : OK |300 : methods wrong | 400讀取失敗	groupName:"" (對象名稱)
}
```



<br>

# 12.更新申請文件
### POST
#### 上傳申請文件
#### path : test/upload_apply_condition_pdf
> 用form
```
request:

{
	file:"" (pdf)
}

response:

{
	rspCOde:"" 200 : OK |300 : methods wrong | 400 : 圖片上傳錯誤 | 401 : 檔案類型不許可 | 402 : 檔案傳輸方式錯誤、或是檔案超過2MB
}
```

<br>

# 13.檢查申請文件是否存在
### GET
#### 檢查檔案是否存在
#### path : test/output_apply_condition_pdf
```
request:

{
	NULL
}

response:

{	
	fileName:"" (固定)
	rspCOde:"" 200 : OD | 300  : method false | 400 未知 | 401 : 檔案不存在
}
```

# 14.顯示可申請類別
### GET
#### 把可申請的類別列出來
#### path : test/output_apply_class
```
request:

{
	NULL
}

response:

{	
	allClass:"" (list)
	rspCode:"' 200 OK | 300 method wrong | 400 fail
}
```

<br>

# 15.根據所選的class回復可申請的period和其quota 
### POST
#### 
#### path : test/output_quota_conditionID
```
request:

{
	class:"" (輸入大於10個字會報錯)
}

response:

{
	"quotaList":"" (list)
	"rspCode":"200" OK | 201此class沒有可被申請的項目 | 300 method wrong | 400 未知
}
```

<br>

# 16. 新增與更新申請條件
### POST
#### 用於更新與新增
#### path : test/update_add_apply_quota
```
request:

{	
	class:"" (輸入的如果是'其他'或是大於10個字會報錯)
	once:"", one:"", three:"" , six:"", year:""(輸入0代表刪除此申請period或是不新增此項目,可輸入0~99999)(如果沒有變動請傳回原數值)(不可為空)
}

response:

{
	rspCode:"" 200 OK| 300 method wrong | 400 未知 | 401 輸入不合法
}
```

<br>

# 17.刪除申請類別 
### POST
#### 會一次刪光所有此類型的可申請項目
#### path : test/delete_apply_class
```
request:

{
	class:"" (小於10個字)
}

response:

{
	rsoCode :"" 200 OK | 300 method wrong | 400 刪除失敗或是此類型不存在可申請項目
}
```

<br>

# 18.回傳要求的quota和condition id 
### POST
#### 可以只查個別的quota和condition ID
#### path : /test/output_quota_conditionID
```
request:

{
	class:""(小於10個字)
	period:""(0~99999)
}

response:

{
	rspCode:"" 200 OK | 201 其他沒有quota | 300 method wrong |400 class或是period為空	| 401 抓取資料失敗 | 402 沒有此資料
}
```

# 19.使用者新增申請
### POST
#### 使用者按下送出申請的動作
#### path : test/USER/add_apply
> 用form
```
request:

{
	frequency:"" 1~999999 一次性填1
	period:"  	 必須是0,30,90,180,365 對應一次、一個月、三個月、半年、一年
	result:""    如果class為其他就必填，無長度限制
	class:""	 如果不在可申請範圍內會回傳錯誤
	quota:""	 其他自填，正常的留空
	file(pdf):"" 可有可無
}

response:

{
	rspCode:""	200 OK| 300 method wrong | 400 未知 |401 找不到conditionID | 402 其他要填原因 | 403 有輸入不符合格式 | 404 pdf上傳錯誤
	notAllow:"" 會把有問題的輸入的request名傳回
}
```


<br>

# 20.未審核申請資料顯示 
### POST
#### 列出未審核的資料
#### path : /test/show_apply_status_0
```
request:

{
	name:"" 你要搜尋的目標 20個字內
}

response:

{
	rspCode:"" 200 OK | 300 method wrong | 400 未知 | 401 target太長

	以下是list
	userNam:""
	userSRRate:""
	userSPRate:""
	applyPdfName:""
	applyID:""
	applyClass:""
	applyQuota:""
	applyPeriod:""
	applyFrequency:""
	applyTime:""
	applyResult:""
	userID:""

}
```

<br>

# 21.審核申請頁面中的簡略紀錄 
### POST
#### 滑到申請人身上會跑出來的
#### path : /test/simple_personal_apply_history
```
request:

{
	applyID:"" 滑到哪個傳哪個
	
}

response:

{
	rsoCode:"" 200 OK | 300 method wrong | 400 applyID 不存在

	以下是list
	applyTime:""
	frequency:""
	result:""
	status:"" 
	judgeTime:"" 
	period:"" 
	className:""
	quota:""
	oldQuota:"" 
	applyPdfName:"" 
	applyID:""
	userID:"" 
	userName:""
}
```

<br>

# 22.申請附件下載 
### POST
#### 使用此api理論上會直接跳出下載的視窗
#### path : /test/apply_pdf_download
```
request:

{
	applyID 要幾號傳幾號
}

response:

{
	200 OK | 300 method wrong | 400 檔案不存在
}
```

<br>

# 23.決定申請是否通過 
### POST
#### 審核apply用
#### path : /test/apply_pdf_download
```
request:

{
	applyID :"" 要審核哪個傳哪個,
	applyStatus :"" (案的是核准就給1沒過給2),
	quotaChange :"" (核准額度有變給值，沒有傳空)
}

response:

{
	200 OK | 300 method wrong | 400 有非法輸入
	notAllow 會把有問題的輸入的request名傳回
}
```

<br>

# 24.核准紀錄 
### POST
#### 完整的核准紀錄
#### path : /test/judgement_history
```
request:

{
	這裡亂輸入不會出事，只是查不到東西而已
	name :"" 
	status :""  (1 or 2)
	class :"" 
	period :"" (0,30,90,180,365)
}

response:

{
	200 OK | 300 method wrong | 400 未知

}
```

<br>


# 25.顯示user名單 
### POST
#### 在主動配發頁面用的
#### path : /test/show_user
```
request:

{
	target:"" 沒搜尋傳空(沒搜尋)
}

response:

{
	200 OK | 300 method wrong | 400 查找資料失敗(不是沒找到東西，是資料庫壞了))
	以下是list
	name:""
	userID:""
	userSRRate:
	userSPRate:""

}
```

<br>

# 26.配發按鍵 
### POST
#### 在主動配發頁面用的
#### path : /test/allotment
```
request:

{
	kind:"" 	(one or all)
	receiver:""	(one時是目標的ID(), all是搜尋了什麼)
	period:""	(0, 30, 90, 180, 365)
	frequency:""	(一次性傳1)(1~99999)()
	quota:""    (1~99999)
	adminID:"" 測試用(數字的adminID)))
}

response:

{
	200 OK | 300 method wrong | 400  #可能是userID不存在  測試版還可能是adminID不存在
	notAllow:"" 會把有問題的輸入的request名傳回

}
```


<br>

# 27.簡易個人配發紀錄 
### POST
#### 要哪個人就會顯示哪個人的
#### path : /test/simple_allotment_history
```
request:

{
	userID:"" 要哪個人就傳哪個
}

response:

{
	200 OK | 300 method wrong | 400 userID有問題	
	以下是list
	period:[] 
	frequency:[]
	quota:
	time:[]

}
```

<br>

# 27.主動配發紀錄
### POST
#### 要哪個人就會顯示哪個人的
#### path : /test/simple_allotment_history
```
request:

{
	target:"" 沒有搜尋傳空
}

response:

{
	200 OK | 300 method wrong | 400 未知
	period:[]
	frequency:[] 
	quota:[] 
	time:[]
	userID:[] 
	name:[]
}
```

<br>

# 28.新增任務
### POST
#### SR新增任務
#### path : /test/SR/add_task
```
request:

{
	taskName:"" 不為空,小於20個字
	taskStartTime:"" 格式 yyyy-mm-dd hh:mm:ss 
	taskStartTime:"" 格式 yyyy-mm-dd hh:mm:ss 
	taskPoint:"" (0~99999)
	taskLocation:"" 不限制
	taskContent:"" 不限制
	userID:"" 測試用，正式從sessions拿
}

response:

{
	rspCode:""  200 OK |300 method wrong| 400 輸入有問題|401 taskContent有符號出問題
	notAllow:[] 輸入格式有問題的會在這裡
	taskConflit:[
		{
            "taskID": "",
            "taskName": ""
        }
	]			
	pointConflit:"" 會顯示user缺多少錢 like: -100

}
```

<br>

# 29.顯示可接任務
### POST(正式時不傳東西應該是GET)
#### SP顯示可接任務
#### path : /test/SP/output/task_can_be_taken
```
request:

{
	userID:"" 正式時從session拿，必須是數字且存在，不燃會炸
}

response:

{
	rspCode:"" 200 OK |300 method wrong|400 userID 有問題
	taskList:[
		taskID:"",
		taskName:"",
		taskStartTime"",(yy-mm-dd hh:mm:ss)
		taskEndTime:"",(yy-mm-dd hh:mm:ss)
		taskPoint:"",
		SRName:"",
		taskLocation:"",
		taskContent:""
	]
}
```

<br>

# 30.承接任務
### POST
#### SP承接任務的動作
#### path : /test/SP/taken_task
```
request:

{
	userID:"" 正式時從session拿，必須是數字且存在，不燃會炸
	taskID_:"" 要接的那一個
}

response:

{
	rspCode:"" 200 OK |300 method wrong|400 u未知| 401 已申請過此任務| 402 此任務已有SP| 403 任務不存在| 404 時間有衝突
	"taskConflit": 
        {
            "taskID": "",
            "taskName": ""
        }
}
```

<br>

# 30.顯示雇主已發布任務
### POST
#### 雇主已發布頁面用
#### path : /test/SR/output/release
```
request:

{
	userID:"" 正式時從session拿，必須是數字且存在，不燃會炸
	taskID_:"" 要接的那一個
}

response:

{
	rspCode:"" 200 OK |300 method wrong|400 未知| 401 已申請過此任務| 402 此任務已有SP| 403 任務不存在| 404 時間有衝突
	taskAmount:""
	taskList: [
        {
            "CandidateList": [
				userName,
				userID (int)
				],
            "cadidateAmount": "",
            "taskContent": "",
            "taskEndTime": "",
            "taskID": "",
            "taskLocation": "",
            "taskName": "",
            "taskPoint": "",
            "taskStartTime": "",
            "taskStatus": ""
        }
	}
}
```
<br>

# 31.編輯任務
### POST
#### 只能編輯自己的且沒有候選人的
#### path : /test/SR/edit_task
```
request:

{
	userID:"" 正式時從session拿，必須是數字且存在，不燃會炸,
	taskContent: "" 不限制,
    "taskEndTime": "", (yy-mm-dd hh:mm:ss)
    "taskID": "",    改哪個就輸入哪個
    "taskLocation": "" 不限制,
    "taskName": "" 20個字內,
    "taskPoint": "" 0~99999,
    "taskStartTime": "" (yy-mm-dd hh:mm:ss)
}

response:

{
	rspCode:"" 200 OK |300 method wrong|400 任務不存在| 401 任務已有人申請| 402 任務點數或是時間不允許| 403 taskContent符號有問題
	notAllow:[], 會把有問題的輸入的request名傳回
	taskConflit:{
		taskID:"",
		taskName:""
	},
	pointConflit:""	會顯示user缺多少錢 like: -100
}
```

<br>

# 32.雇主確定雇員
### POST
#### 確認SP
#### path : /test/SR/edit_task
```
request:

{
	userID:"" 正式時從session拿，必須是數字且存在，不燃會炸,
	candidateID:"" 傳送SP的userID
	taskID:""	
}

response:

{
	rspCode:"" 200 OK |300 method wrong|400 未知| 401 cadidateID不再候選人名單| 402 userID 非本任務SR
	
}
```
<br>

# 32.雇主已接受頁面
### POST	
#### 顯示雇主已接受的任務
#### path : /test/SR/output/accept
```
request:

{
	userID:"" 正式時從session拿，必須是數字且存在，不燃會炸
}

response:

{
	rspCode:"" 200 OK |300 method wrong|400 user不存在
    taskAmount: "", 有幾個task
    taskList: [
        {
            taskConten: "",
            taskEndTime: "",
            taskID: "",
            taskLocation: "",
            taskName: "",
            taskPoint: "",
            taskSPName: "",
            taskStartTime: ""
       }
    ]
	
}
```

<br>

# 33.雇主刪除任務
### POST	
#### 雇主可刪除還沒有SP的任務
#### path : /test/SR/output/accept
```
request:

{
	userID:"" 正式時從session拿，必須是數字且存在，不燃會炸
}

response:

{
	rspCode:"" 200 OK |300 method wrong|400 任務不存在| 401  任務發放人不是你不能刪除|402 已經有SP| 403 userID 有問題
}
```

<br>

# 34.雇主取消
### POST	
#### 發出取消申請和接受都是這支，不接受不需要使用
#### path : /test/SR/cancel_task
```
request:

{
	userID:"" 正式時從session拿，必須是數字且存在，不燃會炸
	taskID:"" 傳要取消的任務
}

response:

{
	rspCode:"" 200 OK |300 method wrong|400 任務不存在| 401  任務發放人不是你不能取消|402 任務不可取消
}
```


<br>

# 35.雇員取消
### POST	
#### 發出取消申請和接受都是這支，不接受不需要使用
#### path : /test/SP/cancel_task
```
request:

{
	userID:"" 正式時從session拿，必須是數字且存在，不燃會炸
	taskID:"" 傳要取消的任務
}

response:

{
	rspCode:"" 200 OK |300 method wrong|400 任務不存在| 401  任務執行人不是你不能取消|402 任務不可取消
}
```

<br>

# 36.完成或未完成 
### POST	
#### SP、SR共用
#### path : /test/task_finish_or_not	
```
request:

{
	userID:"" 正式時從session拿，必須是數字且存在，不燃會炸
	taskID:"" 傳要取消的任務
	status:"" 0(未完成) or 1 (完成)
}

response:

{
	rspCode:"" 200 OK |300 method wrong|400 任務不存在| 401  任務結束時間未到|402 任務的status不允許評價
}
```

<br>

# 37.完成或未完成 
### POST	
#### SP、SR共用
#### path : /test/task_finish_or_not	
```
request:

{
	userID:"" 正式時從session拿，必須是數字且存在，不燃會炸
	taskID:"" 傳要決定的任務
	status:"" 0(未完成) or 1 (完成)
}

response:

{
	rspCode:"" 200 OK |300 method wrong|400 任務不存在| 401  任務結束時間未到|402 任務的status不允許評價
}
```

<br>

# 38.評論資料顯示 
### POST	
#### SP、SR共用 顯示用戶評論時需要看到的資料
#### path : /test/output/notice_comment	
```
request:

{
	userID:"" 正式時從session拿，必須是數字且存在，不燃會炸
	taskID:"" 傳要評論的任務
}

response:

{
	rspCode:"" 200 OK |300 method wrong|400 任務不存在| 401  userID錯誤|402 userID不是此任務SR或SP |403 還不可評論
}
```

<br>

# 39.評論動作 
### POST	
#### SP、SR共用 
#### path : /test/comment_action
```
request:

{
	userID:"" 正式時從session拿，必須是數字且存在，不燃會炸
	taskID:"" 傳要評論的任務
	comment:"" 無限制,
	star:"" 1,2,3,4,5
}

response:

{
	rspCode:"" 200 OK |300 method wrong|400 任務不存在 | 401  userID不是此任務SR或SP|402  此任務還不可評論| 403 star 不合法| 404 已經評論過
}
```

<br>

# 40.GM審核評論頁面 
### GET	
#### 不須傳值
#### path : /test/GM/output/judge_comment_page
```
request:

{
	NULL
}
	
response:

{
	rspCode:"" 200 OK |300 method wrong|400 userType不是GM | 401  未知
	commentAmount: "",
    commentList": [
        {
            SPComment: "",
            SPID: "",
            "SPName": "",
            "SPPhone": "",
            "SPStar": "",
            "SRComment": "",
            "SRID": "",
            "SRName": "",
            "SRPhone": "",
            "SRStar": "",
            "taskConent": "",
            "taskEndTime": "",
            "taskID": "",
            "taskName": "",
            "taskStartTime": ""
        }
    ]
}
```

<br>

# 41.GM審核評論動作 
### GET	
#### 不須傳值
#### path : /test/GM/judge_commentaction
```
request:

{	
	adminID:"" 正式時從session拿，必須是數字且存在，不燃會炸
	taskID:"" 目標ID
	status:"" 0(不核准),1(核准)
}
	
response:

{
	rspCode:"" 200 OK |300 method wrong|400 commeny不存在 | 401  status不合法| 402 adminID不合法
}
```


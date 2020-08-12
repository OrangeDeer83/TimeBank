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
#### path : /test/USER/detect_repeated
>tip : JavaScript can use onkeyup
```
request:

{
	userID: "" (max length 20)
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
#### path : /test/USER/Register
```
request:

{
	userName: "",		(max length 20)
	userID: "",			(max length 20)
	userPassword: "",	(max length 30)
	userMail: "",		(max length 50)
	userPhone: "",		(max length 20)
	userGender: "",		0:male | 1:female | 2:other
	userBirthday: ""
}

response:

{
	rspCode: ""		200:success | 300:method使用錯誤 | 400:資料庫錯誤 | 401:名稱長度不符 | 402:帳號格式不符 | 403:密碼格式不符 | 404:信箱長度不符 | 405:信箱格式不符 | 406:電話格式不符 | 407:性別異常 | 408:生日格式不符 | 409:未來人錯誤 | 410:帳號重複 | 411:信箱重複
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
	userID: "",			(max length 20)
	userPassword: ""	(max length 30)
}

response:

{
	rspCode: "",		200:登入成功 | 300:method使用錯誤 | 400:資料庫錯誤 | 401:登入失敗
	URL: ""
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
	rspCode: ""		200:重置信寄送成功 | 300:method使用錯誤 | 400:資料庫錯誤 | 401:信箱長度不符 | 402:信箱格式不符 | 403:信箱輸入錯誤，沒有找到對應的信箱 | 404:重置信寄送失敗
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

# API 7 - SA Detect Repeated
### POST
#### 在SA新增管理員時避免帳號重複
#### path : /test/SA/detect_repeated
```
request:

{
	adminID: ""		(max length 20)
}

response:

{
	rspCode: ""		200:沒有重複 | 300:method使用錯誤 | 400: 資料庫錯誤 | 401:帳號格式不符 | 402:偵測到重複帳號
}
```

<br>

# API 7 - Create Admins
### POST
#### SA新增管理員
#### path : /test/create_admins
```
request:

{
	adminType: ""		2:AS | 3:AA | 4:AU | 5:AG
	adminID: ""		 	(max length 20)
	adminPassword: ""	(max length 30)
}

response:

{
	rspCode: ""			200:管理員新增成功 | 300:method使用錯誤 | 400:資料庫錯誤 | 401:管理員權限不符 | 402:帳號格式不符 | 403:密碼格式不符 | 404:帳號重複
}
```

<br>

# API 8 - Delete Admin
### POST
#### SA刪除管理員
#### path : /test/delete_admin
>我想讓SA輸入一次密碼再進行刪除的動作，第一次點擊刪除(SAPassword留空)顯示輸入密碼，輸入一次後就不必再輸入
```
request:

{
	adminID: ""			(max length 20)
	SAPassword: ""		(max length 30)
}

response:

{
	rspCode: ""			200:刪除成功 | 300:method使用錯誤 | 400:資料庫錯誤 | 401:尚未輸入第一次密碼 | 402:adminID不在資料庫中，前端可能遭到竄改 | 403:
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
### path:upload_news
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
### path:/edit_news/<number>
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
	沒有
}
response:

{
	rspCode: ""		200 : OK |300 : methods wrong | 400:title刪除失敗or不存在此news | 401:圖片不存在 | 402:圖片刪除失敗 | 403:內文刪除失敗
}
```
<br>

# 下面是apply的部分

# 9.更新申請對象
### POST
### 更新申請對象
### path:test//update_apply_group

```
request:

{
	groupName: ""	(對象名稱)
}
response:

{
	rspCode: ""		200 : OK |300 : methods wrong | 400(寫入失敗)
}
```

# 10.顯示申請對象
### GET
### 傳申請對象是什麼
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

# 11.顯示可用的news number
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

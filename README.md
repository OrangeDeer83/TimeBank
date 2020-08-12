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
#### use for detect if the userID repeated
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
#### register the user account
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
#### for all user to login
#### path : /test/USER/login
```
request:

{
	type: "",	0:no login | 1:USER | 2:AS | 3:AA | 4:AU | 5:AG | 6:GM | 7:SA
	userID: "",			(max length 20)
	userPassword: ""	(max length 30)
}

response:

{
	rspCode: "",	200:登入成功 | 300:method使用錯誤 | 400:資料庫錯誤 | 401:登入失敗
	URL: ""
}
```

<br>

# API 4 - Logout
### GET
#### for all user to logout
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

# API 5 - USER Forget Password
### POST 
#### for user to apply the email to reset password
#### path : /test/USER/forget_password
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
#### for user to reset the password
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

# API 7 - Create Admins
### POST
#### for SA to create admins
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
#### for SA to delete admin
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
1. 網站介紹存在static\uploadFile\webIntro.txt
2. 最新消息圖片存在static\uploadFile\newsImage\number.jpg
3. 最新消息內文存在static\uploadFile\newsContent\number.txt

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

```request:

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

```request

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
### GET
#### 
#### path : 
```
request:

{
	class:"" (輸入大於10個字會報錯)
}

response:

{
	"periodList":"" (0,30,90,180,365)以天數表示(list)
	"quotaList":"" (list)
	"rspCode":"200" OK | 201此class沒有可被申請的項目 | 300 method wrong | 400 未知
}
```

<br>

# 16. 新增與更新申請條件
### 
#### 用於更新與新增
#### path : 
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
#### path : 
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
### GET
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

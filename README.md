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


# 下面先別看
---

<br>

# API 5 - Upload Web Intro
### POST
#### upload the introdruction of website
#### path : /upload_web_intro
```
request:

{
	intro: ""
}

response:

{
	rspCode: ""		200:success | 300:methods wrong | 400:failed
}

```

<br>

# API 6 - Output Web Intro
### GET
#### output the introduction of the website, for editing or general user to watch
#### path : /output_webIntro
```
request:

{
	null
}

response:

{
	rspCode: "",	200:success | 300:methods wrong | 400:failed
	intro: ""
}
```

<br>

# API 7 - Upload News
### POST
#### upload the photo, title and content of the news
#### path : /upload_news
>tip : use the form to upload the news NOT JAVASCRIPT. The file, title and image in the request should be the name of the input tag in the form. Thus, who make the html also should do this part.
```
request:

{
	file: "",
	title: "",		(max length 30)
	content: ""
}

response:

{
	rspCode: ""     200:success | 300:methods wrong | 400:標題、內文、圖片有空值 | 401:圖片檔名錯誤 | 402:圖片上傳錯誤 | 403:內文上傳錯誤 | 404:標題上傳錯誤
}
```

<br>

# API 8 - Output News Image
### GET
#### ouput the image of news, use for editing and general to watch
#### path : /output_news_image/<number>
>tip : number is the parameter indicate the serial of news
```
request:

{
	null
}

response:

{
	rspCode: "",	200:success | 300:methods wrong | 400:failed
	img: ""
}
```

<br>

# API 9 - Output News Content
### GET
#### uput the content of news, use for editing and general to watch
#### path : /output_news_content/<number>
```
request:

{
	null
}

response:

{
	rspCode: "",	200:success | 300:methods wrong | 400:failed
	content: ""
}
```

<br>

# API 10 - Output News Title
### GET
#### Output the title of news, use for editing and general to watch
#### path : /output_news_title/<number>
```
request:

{
	null
}

response:

{
	rspCode: "",	200:success | 300:methods wrong | 400:failed
	title: ""
}
```

<br>

# API 11 Edit News
### POST
#### edit the news including title, image and content
#### path : /edit_news/<number>
```
request:

{
	title: "",
	img: "",
	content: ""
}

response:

{
	rspCode: ""		200:success | 300:methods wrong | 400:圖片檔名錯誤 | 401:圖片更新失敗 | 402:標題更新錯誤 | 403:內文更新失敗
}
```

<br>

# API 12 - Delete News
### POST
#### delete the news on the portal site
#### path : /delete_news/<number>
```
request:

{
	null
}

response:

{
	rspCode: ""		200:success | 300:methods wrong | 400:database delete error | 401:image doesn't exist | 402:image delete error | 403:content delete error
}
```

<br>

# API 13 - Update Apply Group
### POST
#### update the name of apply group
#### path : /update_apply_group
```
request:

{
    groupName: ""
}

response:

{
	rspCode: ""     200:success | 300:methods wrong | 400:update apply group failed
}
```

<br>

# API 14 - Output Apply Group
### GET
#### output the name of apply group
#### path : /output_apply_group
```
request:

{
    null
}

response:

{
    rspCode: ""     200:success | 300: methods wrong | 400:file access failed
}
```

<br>

# API 15 - Add Apply Class
### POST
#### add and update quota of the class and period
#### path : 
```
request:

{
    class: "",
    once: "",       (max amount 1~99999)
    one: "",        (max amount 1~99999)
    three: "",      (max amount 1~99999)
    six: "",        (max amount 1~99999)
    year: ""        (max amount 1~99999)
}

response:

{
	rspCode: ""     200:success | 
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

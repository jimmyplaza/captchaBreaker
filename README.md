# captchaBreaker
Automatic break captcha &amp; continue crawling(every min) at background, data will be parsed into mongodb.

How to run ? 
======
PRODUCT:


captchaBreaker> run.bat

ps: modify parameters of run.bat to what you want.

DEVELOP:

Usage: <br>

Please input hostname & username & password & apihost & pagelimit <br>

EX: python main.py [hostname] [username] [password] [apihost] [pagelimit]

Mongo Schema:
======
dbname: “tigerdb”   <br>
collection name: “unpaids”    # unpaids customer info <br>
collection name: “paids”      # unlock paid item from brain API<br>
collection name: “histories”  # paid history<br>

EX: <br>

	"_id" : ObjectId("55dc221e764cf03c0903a56f"),  
	"bankcharge" : null,  				#銀行手續費
	"bankfullname" : "国家开发银行",  		#銀行全名 
	"account" : "no98888",  			#會員帳號 
	"create_date" : "2015-08-25 16:06:54",  	#創立時間
	"name" : "陈帅帅", 				#卡主姓名 
	"bankname" : null,  				#銀行名稱 
	"url" : "http://ma1234.hy3858.com:8088/MemberwithdawfundOp/index/done/1304",  #後台URL 
	"money" : "103",   				#出款金額 
	"quota" : "103",  				#提出額度 
	"bankaccount" : "8888888888888888888888",  	#會員銀行帳戶
	"status" : "unpaid",   				#付款狀態
	"boid" : "1304",     				#後台的id 
	"chargepoint" : "0",  				#手續費扣點 
	"condition" : null   				#出款狀況 



Build on windows:
======
Run at windows, execute buildbat.bat

>> buildbat.bat

Find the importer.exe at [dist] directory.


bankmap:
bankmap = """<option value="0">中国工商银行</option><option value="1">中国农业银行</option><option value="2">中国银行</option><option value="3">中国建设银行</option><option value="4">交通银行</option><option value="5">中信银行</option><option value="6">中国光大银行</option><option value="7">华夏银行</option><option value="8">广州发展银行</option><option value="9">平安银行</option><option value="10">招商银行</option><option value="11">兴业银行</option><option value="12">上海浦东发展银行</option><option value="13">北京银行</option><option value="14">天津银行</option><option value="15">河北银行</option><option value="16">邯郸市商业银行</option><option value="17">邢台银行</option><option value="18">张家口市商业银行</option><option value="19">承德银行</option><option value="20">沧州银行</option><option value="21">廊坊银行</option><option value="22">衡水银行</option><option value="23">晋商银行</option><option value="24">晋城银行</option><option value="25">内蒙古银行</option><option value="26">包商银行</option><option value="27">鄂尔多斯银行</option><option value="28">大连银行</option><option value="29">鞍山市商业银行</option><option value="30">锦州银行</option><option value="31">葫芦岛银行</option><option value="32">营口银行</option><option value="33">阜新银行</option><option value="34">吉林银行</option><option value="35">哈尔滨银行</option><option value="36">龙江银行</option><option value="37">南京银行</option><option value="38">江苏银行</option><option value="39">苏州银行</option><option value="40">江苏长江商行</option><option value="41">杭州银行</option><option value="42">宁波银行</option><option value="43">宁波通商银行股份有限公司</option><option value="44">温州银行</option><option value="45">嘉兴银行</option><option value="46">湖州银行</option><option value="47">绍兴银行</option><option value="48">浙江稠州商业银行</option><option value="49">台州银行</option><option value="50">浙江泰隆商业银行</option><option value="51">浙江民泰商业银行</option><option value="52">福建海峡银行</option><option value="53">厦门银行</option><option value="54">泉州银行</option><option value="55">南昌银行</option><option value="56">九江银行股份有限公司</option><option value="57">赣州银行</option><option value="58">上饶银行</option><option value="59">齐鲁银行</option><option value="60">青岛银行</option><option value="61">齐商银行</option><option value="62">枣庄银行</option><option value="63">东营银行</option><option value="64">烟台银行</option><option value="65">潍坊银行</option><option value="66">济宁银行</option><option value="67">泰安市商业银行</option><option value="68">莱商银行</option><option value="69">威海市商业银行</option><option value="70">德州银行</option><option value="71">临商银行</option><option value="72">日照银行</option><option value="73">郑州银行</option><option value="74">中原银行</option><option value="75">洛阳银行</option><option value="76">平顶山银行</option><option value="77">焦作市商业银行</option><option value="78">漯河市商业银行</option><option value="79">汉口银行</option><option value="80">湖北银行</option><option value="81">长沙银行</option><option value="82">广州银行</option><option value="83">珠海华润银行</option><option value="84">广东华兴银行</option><option value="85">广东南粤银行</option><option value="86">东莞银行</option><option value="87">广西北部湾银行</option><option value="88">柳州银行</option><option value="89">桂林银行股份有限公司</option><option value="90">成都银行</option><option value="91">重庆银行</option><option value="92">自贡市商业银行</option><option value="93">攀枝花市商业银行</option><option value="94">德阳银行</option><option value="95">绵阳市商业银行</option><option value="96">南充市商业银行</option><option value="97">贵阳银行</option><option value="98">富滇银行</option><option value="99">西安银行</option><option value="100">长安银行</option><option value="101">兰州银行</option><option value="102">青海银行</option><option value="103">宁夏银行</option><option value="104">乌鲁木齐市商业银行</option><option value="105">昆仑银行</option><option value="106">江阴农商银行</option><option value="107">太仓农商行</option><option value="108">昆山农村商业银行</option><option value="109">吴江农村商业银行</option><option value="110">常熟农村商业银行</option><option value="111">张家港农村商业银行</option><option value="112">广州农村商业银行</option><option value="113">顺德农村商业银行</option><option value="114">海口联合农村商业银行</option><option value="115">重庆农村商业银行</option><option value="116">恒丰银行</option><option value="117">浙商银行</option><option value="118">天津农商银行</option><option value="119">渤海银行</option><option value="120">徽商银行</option><option value="121">北京顺义银座村镇银行</option><option value="122">浙江景宁银座村镇银行</option><option value="123">浙江三门银座村镇银行</option><option value="124">江西赣州银座村镇银行</option><option value="125">东营莱商村镇银行股份有限公司</option><option value="126">深圳福田银座村镇银行</option><option value="127">重庆渝北银座村镇银行</option><option value="128">重庆黔江银座村镇银行</option><option value="129">上海农商银行</option><option value="130">深圳前海微众银行</option><option value="131">上海银行</option><option value="132">北京农村商业银行</option><option value="133">吉林农村信用社</option><option value="134">江苏省农村信用社联合社</option><option value="135">浙江省农村信用社</option><option value="136">鄞州银行</option><option value="137">安徽省农村信用社联合社</option><option value="138">福建省农村信用社</option><option value="139">山东省农联社</option><option value="140">湖北农信</option><option value="141">武汉农村商业银行</option><option value="142">深圳农商行</option><option value="143">东莞农村商业银行</option><option value="144">广西农村信用社</option><option value="145">海南省农村信用社</option><option value="146">四川省联社</option><option value="147">云南省农村信用社</option><option value="148">黄河农村商业银行</option><option value="149">中国邮政储蓄银行</option><option value="150">东亚银行</option><option value="151">友利银行</option><option value="152">新韩银行中国</option><option value="153">企业银行</option><option value="154">韩亚银行</option><option value="8888">民生银行</option>"""





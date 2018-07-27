# -*- coding: utf-8 -*-
import requests
import shutil
from PIL import Image
from PIL import ImageFilter
from pytesser import *
from bs4 import BeautifulSoup
import time
import sys
import pymongo
from bson.objectid import ObjectId
import datetime
import logging
import os
import threading

logging_format='%(asctime)s %(filename)s:%(lineno)d func:%(funcName)s() %(levelname)s  %(name)s MESSAGE: %(message)s'
logging.basicConfig(level=logging.ERROR, format=logging_format, filename='./importer.log')
logger = logging.getLogger(__name__)

# global variable
#bankmap = """<option value="0">中国工商银行</option><option value="1">中国农业银行</option><option value="2">中国银行</option><option value="3">中国建设银行</option><option value="4">交通银行</option><option value="5">中信银行</option><option value="6">中国光大银行</option><option value="7">华夏银行</option><option value="8">广东发展银行</option><option value="9">平安银行</option><option value="10">招商银行</option><option value="11">兴业银行</option><option value="12">上海浦东发展银行</option><option value="13">北京银行</option><option value="14">天津银行</option><option value="15">河北银行</option><option value="16">邯郸市商业银行</option><option value="17">邢台银行</option><option value="18">张家口市商业银行</option><option value="19">承德银行</option><option value="20">沧州银行</option><option value="21">廊坊银行</option><option value="22">衡水银行</option><option value="23">晋商银行</option><option value="24">晋城银行</option><option value="25">内蒙古银行</option><option value="26">包商银行</option><option value="27">鄂尔多斯银行</option><option value="28">大连银行</option><option value="29">鞍山市商业银行</option><option value="30">锦州银行</option><option value="31">葫芦岛银行</option><option value="32">营口银行</option><option value="33">阜新银行</option><option value="34">吉林银行</option><option value="35">哈尔滨银行</option><option value="36">龙江银行</option><option value="37">南京银行</option><option value="38">江苏银行</option><option value="39">苏州银行</option><option value="40">江苏长江商行</option><option value="41">杭州银行</option><option value="42">宁波银行</option><option value="43">宁波通商银行股份有限公司</option><option value="44">温州银行</option><option value="45">嘉兴银行</option><option value="46">湖州银行</option><option value="47">绍兴银行</option><option value="48">浙江稠州商业银行</option><option value="49">台州银行</option><option value="50">浙江泰隆商业银行</option><option value="51">浙江民泰商业银行</option><option value="52">福建海峡银行</option><option value="53">厦门银行</option><option value="54">泉州银行</option><option value="55">南昌银行</option><option value="56">九江银行股份有限公司</option><option value="57">赣州银行</option><option value="58">上饶银行</option><option value="59">齐鲁银行</option><option value="60">青岛银行</option><option value="61">齐商银行</option><option value="62">枣庄银行</option><option value="63">东营银行</option><option value="64">烟台银行</option><option value="65">潍坊银行</option><option value="66">济宁银行</option><option value="67">泰安市商业银行</option><option value="68">莱商银行</option><option value="69">威海市商业银行</option><option value="70">德州银行</option><option value="71">临商银行</option><option value="72">日照银行</option><option value="73">郑州银行</option><option value="74">中原银行</option><option value="75">洛阳银行</option><option value="76">平顶山银行</option><option value="77">焦作市商业银行</option><option value="78">漯河市商业银行</option><option value="79">汉口银行</option><option value="80">湖北银行</option><option value="81">长沙银行</option><option value="82">广州银行</option><option value="83">珠海华润银行</option><option value="84">广东华兴银行</option><option value="85">广东南粤银行</option><option value="86">东莞银行</option><option value="87">广西北部湾银行</option><option value="88">柳州银行</option><option value="89">桂林银行股份有限公司</option><option value="90">成都银行</option><option value="91">重庆银行</option><option value="92">自贡市商业银行</option><option value="93">攀枝花市商业银行</option><option value="94">德阳银行</option><option value="95">绵阳市商业银行</option><option value="96">南充市商业银行</option><option value="97">贵阳银行</option><option value="98">富滇银行</option><option value="99">西安银行</option><option value="100">长安银行</option><option value="101">兰州银行</option><option value="102">青海银行</option><option value="103">宁夏银行</option><option value="104">乌鲁木齐市商业银行</option><option value="105">昆仑银行</option><option value="106">江阴农商银行</option><option value="107">太仓农商行</option><option value="108">昆山农村商业银行</option><option value="109">吴江农村商业银行</option><option value="110">常熟农村商业银行</option><option value="111">张家港农村商业银行</option><option value="112">广州农村商业银行</option><option value="113">顺德农村商业银行</option><option value="114">海口联合农村商业银行</option><option value="115">重庆农村商业银行</option><option value="116">恒丰银行</option><option value="117">浙商银行</option><option value="118">天津农商银行</option><option value="119">渤海银行</option><option value="120">徽商银行</option><option value="121">北京顺义银座村镇银行</option><option value="122">浙江景宁银座村镇银行</option><option value="123">浙江三门银座村镇银行</option><option value="124">江西赣州银座村镇银行</option><option value="125">东营莱商村镇银行股份有限公司</option><option value="126">深圳福田银座村镇银行</option><option value="127">重庆渝北银座村镇银行</option><option value="128">重庆黔江银座村镇银行</option><option value="129">上海农商银行</option><option value="130">深圳前海微众银行</option><option value="131">上海银行</option><option value="132">北京农村商业银行</option><option value="133">吉林农村信用社</option><option value="134">江苏省农村信用社联合社</option><option value="135">浙江省农村信用社</option><option value="136">鄞州银行</option><option value="137">安徽省农村信用社联合社</option><option value="138">福建省农村信用社</option><option value="139">农村信用社</option><option value="140">山东省农联社</option><option value="141">湖北农信</option><option value="142">武汉农村商业银行</option><option value="143">深圳农商行</option><option value="144">东莞农村商业银行</option><option value="145">广西农村信用社</option><option value="146">海南省农村信用社</option><option value="147">四川省联社</option><option value="148">云南省农村信用社</option><option value="149">黄河农村商业银行</option><option value="150">中国邮政储蓄银行</option><option value="151">东亚银行</option><option value="152">友利银行</option><option value="153">新韩银行中国</option><option value="154">企业银行</option><option value="155">韩亚银行</option><option value="8888">中国民生银行</option>"""
#bankmap = """<option value="0">中国工商银行</option><option value="1">中国农业银行</option><option value="2">中国银行</option><option value="3">中国建设银行</option><option value="4">交通银行</option><option value="5">中信银行</option><option value="6">中国光大银行</option><option value="7">华夏银行</option><option value="8">广东发展银行</option><option value="9">平安银行</option><option value="10">招商银行</option><option value="11">兴业银行</option><option value="12">上海浦东发展银行</option><option value="13">北京银行</option><option value="14">天津银行</option><option value="15">河北银行</option><option value="16">邯郸市商业银行</option><option value="17">邢台银行</option><option value="18">张家口市商业银行</option><option value="19">承德银行</option><option value="20">沧州银行</option><option value="21">廊坊银行</option><option value="22">衡水银行</option><option value="23">晋商银行</option><option value="24">晋城银行</option><option value="25">内蒙古银行</option><option value="26">包商银行</option><option value="27">鄂尔多斯银行</option><option value="28">大连银行</option><option value="29">鞍山市商业银行</option><option value="30">锦州银行</option><option value="31">葫芦岛银行</option><option value="32">营口银行</option><option value="33">阜新银行</option><option value="34">吉林银行</option><option value="35">哈尔滨银行</option><option value="36">龙江银行</option><option value="37">南京银行</option><option value="38">江苏银行</option><option value="39">苏州银行</option><option value="40">江苏长江商行</option><option value="41">杭州银行</option><option value="42">宁波银行</option><option value="43">宁波通商银行股份有限公司</option><option value="44">温州银行</option><option value="45">嘉兴银行</option><option value="46">湖州银行</option><option value="47">绍兴银行</option><option value="48">浙江稠州商业银行</option><option value="49">台州银行</option><option value="50">浙江泰隆商业银行</option><option value="51">浙江民泰商业银行</option><option value="52">福建海峡银行</option><option value="53">厦门银行</option><option value="54">泉州银行</option><option value="55">南昌银行</option><option value="56">九江银行股份有限公司</option><option value="57">赣州银行</option><option value="58">上饶银行</option><option value="59">齐鲁银行</option><option value="60">青岛银行</option><option value="61">齐商银行</option><option value="62">枣庄银行</option><option value="63">东营银行</option><option value="64">烟台银行</option><option value="65">潍坊银行</option><option value="66">济宁银行</option><option value="67">泰安市商业银行</option><option value="68">莱商银行</option><option value="69">威海市商业银行</option><option value="70">德州银行</option><option value="71">临商银行</option><option value="72">日照银行</option><option value="73">郑州银行</option><option value="74">中原银行</option><option value="75">洛阳银行</option><option value="76">平顶山银行</option><option value="77">焦作市商业银行</option><option value="78">漯河市商业银行</option><option value="79">汉口银行</option><option value="80">湖北银行</option><option value="81">长沙银行</option><option value="82">广州银行</option><option value="83">珠海华润银行</option><option value="84">广东华兴银行</option><option value="85">广东南粤银行</option><option value="86">东莞银行</option><option value="87">广西北部湾银行</option><option value="88">柳州银行</option><option value="89">桂林银行股份有限公司</option><option value="90">成都银行</option><option value="91">重庆银行</option><option value="92">自贡市商业银行</option><option value="93">攀枝花市商业银行</option><option value="94">德阳银行</option><option value="95">绵阳市商业银行</option><option value="96">南充市商业银行</option><option value="97">贵阳银行</option><option value="98">富滇银行</option><option value="99">西安银行</option><option value="100">长安银行</option><option value="101">兰州银行</option><option value="102">青海银行</option><option value="103">宁夏银行</option><option value="104">乌鲁木齐市商业银行</option><option value="105">昆仑银行</option><option value="106">江阴农商银行</option><option value="107">太仓农商行</option><option value="108">昆山农村商业银行</option><option value="109">吴江农村商业银行</option><option value="110">常熟农村商业银行</option><option value="111">张家港农村商业银行</option><option value="112">广州农村商业银行</option><option value="113">顺德农村商业银行</option><option value="114">海口联合农村商业银行</option><option value="115">重庆农村商业银行</option><option value="116">恒丰银行</option><option value="117">浙商银行</option><option value="118">天津农商银行</option><option value="119">渤海银行</option><option value="120">徽商银行</option><option value="121">北京顺义银座村镇银行</option><option value="122">浙江景宁银座村镇银行</option><option value="123">浙江三门银座村镇银行</option><option value="124">江西赣州银座村镇银行</option><option value="125">东营莱商村镇银行股份有限公司</option><option value="126">深圳福田银座村镇银行</option><option value="127">重庆渝北银座村镇银行</option><option value="128">重庆黔江银座村镇银行</option><option value="129">上海农商银行</option><option value="130">深圳前海微众银行</option><option value="131">上海银行</option><option value="132">北京农村商业银行</option><option value="133">吉林农村信用社</option><option value="134">江苏省农村信用社联合社</option><option value="135">浙江省农村信用社</option><option value="136">鄞州银行</option><option value="137">安徽省农村信用社联合社</option><option value="138">福建省农村信用社</option><option value="139">农村信用社</option><option value="140">山东省农联社</option><option value="141">湖北农信</option><option value="142">武汉农村商业银行</option><option value="143">深圳农商行</option><option value="144">东莞农村商业银行</option><option value="145">广西农村信用社</option><option value="146">海南省农村信用社</option><option value="147">四川省联社</option><option value="148">云南省农村信用社</option><option value="149">黄河农村商业银行</option><option value="150">中国邮政</option><option value="150">中国邮政储蓄银行</option><option value="151">东亚银行</option><option value="152">友利银行</option><option value="153">新韩银行中国</option><option value="154">企业银行</option><option value="155">韩亚银行</option><option value="8888">中国民生银行</option>"""

#bankmap = """<option value="0">中国工商银行</option><option value="1">中国农业银行</option><option value="2">中国银行</option><option value="3">中国建设银行</option><option value="4">交通银行</option><option value="5">中信银行</option><option value="6">中国光大银行</option><option value="7">华夏银行</option><option value="8">广发银行</option><option value="9">平安银行（原深圳发展银行）</option><option value="10">招商银行</option><option value="11">兴业银行</option><option value="12">上海浦东发展银行</option><option value="13">北京银行</option><option value="14">天津银行</option><option value="15">河北银行</option><option value="16">邯郸市商业银行</option><option value="17">邢台银行</option><option value="18">张家口市商业银行</option><option value="19">承德银行</option><option value="20">沧州银行</option><option value="21">廊坊银行</option><option value="22">衡水银行</option><option value="23">晋商银行</option><option value="24">晋城银行</option><option value="25">内蒙古银行</option><option value="26">包商银行</option><option value="27">鄂尔多斯银行</option><option value="28">大连银行</option><option value="29">鞍山市商业银行</option><option value="30">锦州银行</option><option value="31">葫芦岛银行</option><option value="32">营口银行</option><option value="33">阜新银行</option><option value="34">吉林银行</option><option value="35">哈尔滨银行</option><option value="36">龙江银行</option><option value="37">南京银行</option><option value="38">江苏银行</option><option value="39">苏州银行</option><option value="40">江苏长江商行</option><option value="41">杭州银行</option><option value="42">宁波银行</option><option value="43">宁波通商银行股份有限公司</option><option value="44">温州银行</option><option value="45">嘉兴银行</option><option value="46">湖州银行</option><option value="47">绍兴银行</option><option value="48">浙江稠州商业银行</option><option value="49">台州银行</option><option value="50">浙江泰隆商业银行</option><option value="51">浙江民泰商业银行</option><option value="52">福建海峡银行</option><option value="53">厦门银行</option><option value="54">泉州银行</option><option value="55">南昌银行</option><option value="56">九江银行股份有限公司</option><option value="57">赣州银行</option><option value="58">上饶银行</option><option value="59">齐鲁银行</option><option value="60">青岛银行</option><option value="61">齐商银行</option><option value="62">枣庄银行</option><option value="63">东营银行</option><option value="64">烟台银行</option><option value="65">潍坊银行</option><option value="66">济宁银行</option><option value="67">泰安市商业银行</option><option value="68">莱商银行</option><option value="69">威海市商业银行</option><option value="70">德州银行</option><option value="71">临商银行</option><option value="72">日照银行</option><option value="73">郑州银行</option><option value="74">中原银行</option><option value="75">洛阳银行</option><option value="76">平顶山银行</option><option value="77">焦作市商业银行</option><option value="78">漯河市商业银行</option><option value="79">汉口银行</option><option value="80">湖北银行</option><option value="81">长沙银行</option><option value="82">广州银行</option><option value="83">珠海华润银行</option><option value="84">广东华兴银行</option><option value="85">广东南粤银行</option><option value="86">东莞银行</option><option value="87">广西北部湾银行</option><option value="88">柳州银行</option><option value="89">桂林银行股份有限公司</option><option value="90">成都银行</option><option value="91">重庆银行</option><option value="92">自贡市商业银行</option><option value="93">攀枝花市商业银行</option><option value="94">德阳银行</option><option value="95">绵阳市商业银行</option><option value="96">南充市商业银行</option><option value="97">贵阳银行</option><option value="98">富滇银行</option><option value="99">西安银行</option><option value="100">长安银行</option><option value="101">兰州银行</option><option value="102">青海银行</option><option value="103">宁夏银行</option><option value="104">乌鲁木齐市商业银行</option><option value="105">昆仑银行</option><option value="106">江阴农商银行</option><option value="107">太仓农商行</option><option value="108">昆山农村商业银行</option><option value="109">吴江农村商业银行</option><option value="110">常熟农村商业银行</option><option value="111">张家港农村商业银行</option><option value="112">广州农村商业银行</option><option value="113">顺德农村商业银行</option><option value="114">海口联合农村商业银行</option><option value="115">重庆农村商业银行</option><option value="116">恒丰银行</option><option value="117">浙商银行</option><option value="118">天津农商银行</option><option value="119">渤海银行</option><option value="120">徽商银行</option><option value="121">北京顺义银座村镇银行</option><option value="122">浙江景宁银座村镇银行</option><option value="123">浙江三门银座村镇银行</option><option value="124">江西赣州银座村镇银行</option><option value="125">东营莱商村镇银行股份有限公司</option><option value="126">深圳福田银座村镇银行</option><option value="127">重庆渝北银座村镇银行</option><option value="128">重庆黔江银座村镇银行</option><option value="129">上海农商银行</option><option value="130">深圳前海微众银行</option><option value="131">上海银行</option><option value="132">北京农村商业银行</option><option value="133">吉林农村信用社</option><option value="134">江苏省农村信用社联合社</option><option value="135">浙江省农村信用社</option><option value="136">鄞州银行</option><option value="137">安徽省农村信用社联合社</option><option value="138">福建省农村信用社</option><option value="139">农村信用社</option><option value="140">山东省农联社</option><option value="141">湖北农信</option><option value="142">武汉农村商业银行</option><option value="143">深圳农商行</option><option value="144">东莞农村商业银行</option><option value="145">广西农村信用社（合作银行）</option><option value="146">海南省农村信用社</option><option value="147">四川省联社</option><option value="148">云南省农村信用社</option><option value="149">黄河农村商业银行</option><option value="150">中国邮政储蓄银行</option><option value="151">东亚银行（中国）有限公司</option><option value="152">友利银行</option><option value="153">新韩银行中国</option><option value="154">企业银行</option><option value="155">韩亚银行</option><option value="8888">中国民生银行</option>"""
#bankmap = """<option value="0" selected="">中国工商银行</option><option value="1" selected="">中国农业银行</option><option value="2" selected="">中国银行</option><option value="3" selected="">中国建设银行</option><option value="4" selected="">交通银行</option><option value="5" selected="">中信银行</option><option value="6" selected="">中国光大银行</option><option value="7" selected="">华夏银行</option><option value="8" selected="">广发银行</option><option value="9" selected="">平安银行（原深圳发展银行）</option><option value="10" selected="">招商银行</option><option value="11" selected="">兴业银行</option><option value="12" selected="">上海浦东发展银行</option><option value="13" selected="">北京银行</option><option value="14" selected="">天津银行</option><option value="15" selected="">河北银行</option><option value="16" selected="">邯郸市商业银行</option><option value="17" selected="">邢台银行</option><option value="18" selected="">张家口市商业银行</option><option value="19" selected="">承德银行</option><option value="20" selected="">沧州银行</option><option value="21" selected="">廊坊银行</option><option value="22" selected="">衡水银行</option><option value="23" selected="">晋商银行</option><option value="24" selected="">晋城银行</option><option value="25" selected="">内蒙古银行</option><option value="26" selected="">包商银行</option><option value="27" selected="">鄂尔多斯银行</option><option value="28" selected="">大连银行</option><option value="29" selected="">鞍山市商业银行</option><option value="30" selected="">锦州银行</option><option value="31" selected="">葫芦岛银行</option><option value="32" selected="">营口银行</option><option value="33" selected="">阜新银行</option><option value="34" selected="">吉林银行</option><option value="35" selected="">哈尔滨银行</option><option value="36" selected="">龙江银行</option><option value="37" selected="">南京银行</option><option value="38" selected="">江苏银行</option><option value="39" selected="">苏州银行</option><option value="40" selected="">江苏长江商行</option><option value="41" selected="">杭州银行</option><option value="42" selected="">宁波银行</option><option value="43" selected="">宁波通商银行股份有限公司</option><option value="44" selected="">温州银行</option><option value="45" selected="">嘉兴银行</option><option value="46" selected="">湖州银行</option><option value="47" selected="">绍兴银行</option><option value="48" selected="">金华银行股份有限公司</option><option value="49" selected="">浙江稠州商业银行</option><option value="50" selected="">台州银行</option><option value="51" selected="">浙江泰隆商业银行</option><option value="52" selected="">浙江民泰商业银行</option><option value="53" selected="">福建海峡银行</option><option value="54" selected="">厦门银行</option><option value="55" selected="">泉州银行</option><option value="56" selected="">南昌银行</option><option value="57" selected="">九江银行股份有限公司</option><option value="58" selected="">赣州银行</option><option value="59" selected="">上饶银行</option><option value="60" selected="">齐鲁银行</option><option value="61" selected="">青岛银行</option><option value="62" selected="">齐商银行</option><option value="63" selected="">枣庄银行</option><option value="64" selected="">东营银行</option><option value="65" selected="">烟台银行</option><option value="66" selected="">潍坊银行</option><option value="67" selected="">济宁银行</option><option value="68" selected="">泰安市商业银行</option><option value="69" selected="">莱商银行</option><option value="70" selected="">威海市商业银行</option><option value="71" selected="">德州银行</option><option value="72" selected="">临商银行</option><option value="73" selected="">日照银行</option><option value="74" selected="">郑州银行</option><option value="75" selected="">中原银行</option><option value="76" selected="">洛阳银行</option><option value="77" selected="">平顶山银行</option><option value="78" selected="">焦作市商业银行</option><option value="79" selected="">汉口银行</option><option value="80" selected="">湖北银行</option><option value="81" selected="">长沙银行</option><option value="82" selected="">广州银行</option><option value="83" selected="">珠海华润银行</option><option value="84" selected="">广东华兴银行</option><option value="85" selected="">广东南粤银行</option><option value="86" selected="">东莞银行</option><option value="87" selected="">广西北部湾银行</option><option value="88" selected="">柳州银行</option><option value="89" selected="">桂林银行股份有限公司</option><option value="90" selected="">成都银行</option><option value="91" selected="">重庆银行</option><option value="92" selected="">自贡市商业银行</option><option value="93" selected="">攀枝花市商业银行</option><option value="94" selected="">德阳银行</option><option value="95" selected="">绵阳市商业银行</option><option value="96" selected="">南充市商业银行</option><option value="97" selected="">贵阳银行</option><option value="98" selected="">富滇银行</option><option value="99" selected="">西安银行</option><option value="100" selected="">长安银行</option><option value="101" selected="">兰州银行</option><option value="102" selected="">青海银行</option><option value="103" selected="">宁夏银行</option><option value="104" selected="">乌鲁木齐市商业银行</option><option value="105" selected="">昆仑银行</option><option value="106" selected="">江阴农商银行</option><option value="107" selected="">太仓农商行</option><option value="108" selected="">昆山农村商业银行</option><option value="109" selected="">吴江农村商业银行</option><option value="110" selected="">常熟农村商业银行</option><option value="111" selected="">张家港农村商业银行</option><option value="112" selected="">广州农村商业银行</option><option value="113" selected="">顺德农村商业银行</option><option value="114" selected="">海口联合农村商业银行</option><option value="115" selected="">成都农村商业银行股份有限公司</option><option value="116" selected="">重庆农村商业银行</option><option value="117" selected="">恒丰银行</option><option value="118" selected="">浙商银行</option><option value="119" selected="">天津农商银行</option><option value="120" selected="">渤海银行</option><option value="121" selected="">徽商银行</option><option value="122" selected="">北京顺义银座村镇银行</option><option value="123" selected="">浙江景宁银座村镇银行</option><option value="124" selected="">浙江三门银座村镇银行</option><option value="125" selected="">江西赣州银座村镇银行</option><option value="126" selected="">东营莱商村镇银行股份有限公司</option><option value="127" selected="">深圳福田银座村镇银行</option><option value="128" selected="">重庆渝北银座村镇银行</option><option value="129" selected="">重庆黔江银座村镇银行</option><option value="130" selected="">上海农商银行</option><option value="131" selected="">深圳前海微众银行</option><option value="132" selected="">上海银行</option><option value="133" selected="">北京农村商业银行</option><option value="134" selected="">吉林农村信用社</option><option value="135" selected="">江苏省农村信用社联合社</option><option value="136" selected="">浙江省农村信用社</option><option value="137" selected="">鄞州银行</option><option value="138" selected="">安徽省农村信用社联合社</option><option value="139" selected="">福建省农村信用社</option><option value="140" selected="">农村信用社</option><option value="141" selected="">山东省农联社</option><option value="142" selected="">湖北农信</option><option value="143" selected="">武汉农村商业银行</option><option value="144" selected="">深圳农商行</option><option value="145" selected="">东莞农村商业银行</option><option value="146" selected="">广西农村信用社（合作银行）</option><option value="147" selected="">海南省农村信用社</option><option value="148" selected="">四川省联社</option><option value="149" selected="">云南省农村信用社</option><option value="150" selected="">黄河农村商业银行</option><option value="151" selected="">中国邮政储蓄银行</option><option value="152" selected="">东亚银行（中国）有限公司</option><option value="153" selected="">友利银行</option><option value="154" selected="">新韩银行中国</option><option value="155" selected="">企业银行</option><option value="156" selected="">韩亚银行</option><option value="8888">中国民生银行</option>"""

bankdict = dict()
conn = None
captcha_image = None
denoise_image = None
pass_factor = None
rs = None
hostname = None
pagelimit = 0
DEBUG = 0
SAVE = 0
histories = None
sleeptime = None
apihost = None
pushbtnlimit = None
page = None


def prepareImage(img):
	"""Transform image to greyscale and blur it"""
	img = img.filter(ImageFilter.SMOOTH_MORE)
	img = img.filter(ImageFilter.SMOOTH_MORE)
	if 'L' != img.mode:
		img = img.convert('L')
	return img

def removeNoise(img, pass_factor):
	for column in range(img.size[0]):
		for line in range(img.size[1]):
			value = removeNoiseByPixel(img, column, line, pass_factor)
			img.putpixel((column, line), value)
	return img

def removeNoiseByPixel(img, column, line, pass_factor):
	if img.getpixel((column, line)) < pass_factor:
		return (0)
	return (255)

def getCaptcha(captcha_image):
    global rs
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
         'Cookie':'Lang=zh-tw; PHPSESSID=8jn8kr89k34pp6hsv28416faa4; _c_aut=WsR3yG5_rH%2Cd%400Ha79%3AnK%2CIPjSP%3ATsZO%2C05JAjcbNUf%2CCn%5B4%40tV%40%60J; _c_cookie=1; _c_cookie2=%2AFJ_-'}
    rs = requests.session()
    rs.headers['Connection'] = 'keep_alive'
    #response  = rs.get('http://ma1234.hy3858.com:8088/Login/authnum', stream=True, headers = header)
    response  = rs.get(hostname + '/Login/authnum', stream=True, headers = header)
    with open(captcha_image, 'wb') as output_file:
        shutil.copyfileobj(response.raw, output_file)
    print rs
    del response

def recognition(output_image):
    captcha_num = image_file_to_string(output_image) # Run tesseract.exe on image
    return captcha_num

def try_except(link, boid, itemName):
    try:
        #print type(link)
        #print link
        #item = link.string
        item = link.text
        return item.strip()
    except Exception as e:
        errmsg = str(boid) + ' ERROR: ' + itemName + " " + str(e)
        print errmsg
        logger.error(errmsg)
        return -1


# Get small page of account html info
def crawlAccountInfo(rs, url):
    d = dict()

    if DEBUG != 1:
        try:
            res = rs.get(url)
        except:
            logger.error("ERROR: get url: " + url)
            return None

        response_text = res.text #already unicode
        soup = BeautifulSoup(response_text, "lxml")


    #lockcheck = soup.find('div', {'class':'modal-body'})
    #if lockcheck != None:
        #lockstr = lockcheck.text.strip()
        #if lockstr.find(u"已锁定") != -1:
            #return -1

    if DEBUG == 1:
        if os.path.exists("info.html"):
            htmldoc = open("info.html",'r').read()
            soup = BeautifulSoup(htmldoc)

    if SAVE == 1:
        print 'Parse customer account info page into info.html'
        #html = soup.prettify("utf-8")
        html = soup
        with open("info.html", "wb") as file:
            file.write(str(html))
        sys.exit(0)


    #soup2 = BeautifulSoup(bankmap, "lxml")
    soup2 = BeautifulSoup(page.read(),"lxml")
    for option in soup2.find_all('option'):
        bankdict[option.text.encode('utf-8')] = option['value']

    d['_id'] = ObjectId()
    d['url'] = url   #於後台的位置
    if DEBUG == 1:
        boid = 9999
    else:
        boid = url.split("/")[-1]
    d['boid'] = boid #於後台的id

    try:
        link = soup.find('div', {'class':'col-md-3'}) #會員帳號
    except:
        errmsg = str(boid) + " account link obj is None"
        print errmsg
        logger.error(errmsg)
        return None
    print link
    account = try_except(link, boid, "account")
    if account == -1:
        return None
    d['account'] = account

    try:
        link = link.findNext('div', {'class':'col-md-3'}) #出款狀況
    except:
        errmsg = str(boid) + " Ocondition link obj is None"
        print errmsg
        logger.error(errmsg)
        return None
    Ocondition = try_except(link, boid, "Ocondition")
    if Ocondition == -1:
        return None
    d['condition'] = Ocondition

    try:
        link = link.findNext('div', {'class':'col-md-3'}) #提出額度
    except:
        errmsg = str(boid) + " Oquota link obj is None"
        print errmsg
        logger.error(errmsg)
        return None
    Oquota = try_except(link, boid, "Oquota")
    if Oquota == -1:
        return None
    d['quota'] = Oquota

    try:
        link = link.findNext('div', {'class':'col-md-3'}) #手續費扣點
    except:
        errmsg = str(boid) + " chargepoint link obj is None"
        print errmsg
        logger.error(errmsg)
        return None
    chargepoint = try_except(link, boid, "chargepoint")
    if chargepoint == -1:
        return None
    d['chargepoint'] = chargepoint

    try:
        link = link.findNext('div', {'class':'col-md-3'}) #出款金額
    except:
        errmsg = str(boid) + " Omoney link obj is None"
        print errmsg
        logger.error(errmsg)
        return None

    if link.label != None:
        Omoney = try_except(link.label, boid, "Omoney")
    else:
        return None
    if Omoney == -1:
        return None
    #if int(Omoney) > moneylimit:
        #print str(Omoney) + ' > ' + str(moneylimit)
        #return -2
    d['money'] = int(Omoney)

    try:
        link = link.findNext('div', {'class':'col-md-3'}) #銀行手續費
    except:
        errmsg = str(boid) + " bankcharge link obj is None"
        print errmsg
        logger.error(errmsg)
        return None
    bankcharge = try_except(link, boid, "bankcharge")
    if bankcharge == -1:
        return None
    d['bankcharge'] = bankcharge

    try:
        link = link.findNext('div', {'class':'col-md-3'}) #卡主姓名
    except:
        errmsg = str(boid) + " name link obj is None"
        print errmsg
        logger.error(errmsg)
        return None

    try:
        #name = link.label.string
        name = link.label.text.encode('utf-8')
    except Exception as e:
        errmsg = str(boid) + ' ERROR: ' + "name" + " " + str(e)
        print errmsg
        logger.error(errmsg)
        return None
    d['name'] = name.strip()


    try:
        link = soup.find('div', {'class':'col-md-4'}) #銀行名稱
    except:
        errmsg = str(boid) + " bankname link obj is None"
        print errmsg
        logger.error(errmsg)
        return None
    try:
        if len(link.contents[0].strip().split(' ')) >= 2 :
            bankname = link.contents[0].strip().split(' ')[1].strip()
        else:
            errmsg = str(boid) + ' ERROR: ' + "bankname"
            print errmsg
            logger.error(errmsg)
            return None
    except Exception as e:
        errmsg = str(boid) + ' ERROR: ' + "bankname" + " " + str(e)
        print errmsg
        logger.error(errmsg)
        return None

    d['bankfullname'] = bankname


    try:
        bname = bankdict.get(bankname.encode('utf-8'))
    except:
        errmsg = str(boid) + " ERROR: bankdict.get(bankname.encode('utf-8')"
        print errmsg
        logger.error(errmsg)
        return None
    d['bankname'] = bname



    try:
        link = link.findNext('div', {'class':'col-md-4'}) #會員銀行帳戶
    except:
        errmsg = str(boid) + " bankaccount link obj is None"
        print errmsg
        logger.error(errmsg)
        return None

    try:
        link = link.find('label',{'id':'Obank'})
    except:
        errmsg = str(boid) + " bankaccount" + " link obj label id Obank is None"
        print errmsg
        logger.error(errmsg)
        return None
    bankaccount = try_except(link, boid, "bankaccount")
    if bankaccount == -1:
        return None
    d['bankaccount'] = bankaccount

    now = datetime.datetime.now()
    d['create_date'] = now.strftime("%Y-%m-%d %H:%M:%S")
    d['status'] = 'unpaid'       #狀態 ( "unpaid" | "paid" | "mark" | "rm-mark" | "padding" | "fail" )

    return d


def save2mongo(collect, urlObj):
    d = dict()
    urldict = dict()

    #find mongo collection, create url diction to check
    for row in collect.find():
        url = row['url']
        urldict[url] = ""

    for obj in urlObj:
        boid = obj.doneurl.split("/")[-1]
        print "<boid: "+boid+">"

        if urldict != {}:
            if obj.doneurl in urldict:  # if url already exist in db, do nothing
                print boid + ' already exist, nothing to do\n'
                continue

        ret = db.paids.find_one({"boid": boid, "status":"paid"})
        if ret is not None:
            msg = 'boid: ' + boid + ' exist in paids collection, nothing to do\n'
            print msg
            logger.error(msg)
            continue

        ret = db.histories.find_one({"boid": boid, "status":"fail"})
        if ret is not None:
            msg = 'boid: ' + boid + ' paid fail, nothing to do\n'
            print msg
            logger.error(msg)
            continue

        ret = db.histories.find_one({"boid": boid, "status":"paid"})
        if ret is not None:
            msg = 'boid: ' + boid + ' has paid, nothing to do\n'
            print msg
            logger.error(msg)
            continue

        if DEBUG != 1:
            rs.get(obj.unlockurl)

        d = crawlAccountInfo(rs, obj.doneurl)
        if d == -1:
            errmsg = 'This ' + boid + ' boid is locked, maybe operated by someone.\n'
            print errmsg
            logger.error(errmsg)
            continue
        if d == -2:
            try:
                rs.get(obj.unlockurl)
            except:
                print 'get unlockurl error'
                continue

            print '\nMoney over limit\n'
            continue

        if d != None:
            #if DEBUG != 1:
                #rs.get(obj.unlockurl)
            crawler.insert(d)
            histories.insert(d)
            print d
            print '\n**************************** Save boid ' + boid + ' to mongo\n'
        else:
            if DEBUG != 1:
                rs.get(obj.unlockurl)
            print boid + ' next turn retry\n'
            continue



def breakCaptcha(user, pwd):
    process = "breaking..."

    while True:
        print process
        getCaptcha(captcha_image)
        try:
            img = Image.open(captcha_image)
        except:
            print 'open captcha_image error, retry'
            #logger.error("open captcah_image error, retry")
            continue
        #img.show()
        #print img.format, img.size, img.mode
        img = img.convert('RGB')
	    #print img.format, img.size, img.mode
        img = prepareImage(img)
        img = removeNoise(img, pass_factor)
        img.save(denoise_image)
        #img.show()

        captcha_num = recognition(denoise_image)
        captcha_num = captcha_num[:5]

        if len(str(captcha_num)) != 5:
	        print 'captcha len not accurate!, please retry'
	        process = process + "."
	        print process
	        continue

        do = False
        try:
	        captcha = int(captcha_num)
	        do = True
        except:
	        print 'Except, please retry'
	        process = process + "."
	        print process
	        continue

        process = process + "."
        print process
        time.sleep(1)
        if do:
            payload = {'login':user,'pass':pwd,'authnum':captcha}
            print rs
            #res = rs.post('http://ma1234.hy3858.com:8088/Login/', data=payload)
            try:
                res = rs.post(hostname + '/Login/', data=payload)
            except:
                #logger.error("post payload error")
                print 'post payload error'
                continue
            htmlText = res.text
            if htmlText.find('data-msg-required') == -1:
	            #print htmlText
	            break

    #org_img = Image.open(captcha_image)
    print '\nCaptcha: ' + str(captcha)

    print 'Break Success!!'


def getWithdrawContent(moneylimit):
    print 'In getWithdrawContent func'
    global rs
    urlObj = []
    allItemNum = 0

    #res = rs.get('http://ma1234.hy3858.com:8088/MemberwithdawfundOp/index')
    res = rs.get(hostname + '/MemberwithdawfundOp/index')
    response_text = res.text.encode('utf8')
    soup = BeautifulSoup(response_text, "lxml")

    for ul in soup.findAll('ul', {'class':'pagination'}):
        pagestr = ul.findAll('li',{'class':'disabled'})[-1].getText()
        for s in pagestr.split():
            if s.isdigit():
                allItemNum = int(s)

    totalpage = int(allItemNum/10) + 1
    print 'totalpage: ' + str(totalpage)

    if allItemNum == 0:
        for alink in soup.findAll('a', {'class':'btn btn-xs bs-tooltip modal-myurl'}):
            #if alink['src'].find('done') !=  - 1 :
            if alink['href'].find('done') !=  - 1 :
                allItemNum = allItemNum + 1
    if allItemNum == 0:
        errmsg = 'allItemNum is zero, return., urlObj = []'
        print errmsg
        logger.error(errmsg)
        return urlObj

    print 'allItemNum: ' + str(allItemNum)
    urlObj = [UrlCollect() for u in range(allItemNum)]

    i = 0
    j = 0
    if totalpage > int(pagelimit):
        totalpage = int(pagelimit)
    print 'limited totalpage: ' + str(totalpage)
    for p in reversed(range(totalpage)):
        p = p + 1
        geturl = hostname + '/MemberwithdawfundOp/index/list/0/' + str(p)
        print 'GET url: ' + geturl
        res = rs.get(geturl)
        response_text2 = res.text.encode('utf8')
        soup = BeautifulSoup(response_text2, "lxml")
        doneurl = []
        unlockurl = []
        j = i
        for tr in soup.findAll('tr'):
            omoney = tr.select('td:nth-of-type(4)')
            if omoney == []:
                continue
            if int(omoney[0].text) <= moneylimit:
                #print omoney[0].text
                for alink in tr.findAll('a', {'class':'btn btn-xs bs-tooltip'}):
                    if alink['href'].find('unlock') != -1:
                        unlockurl.append(alink['href'])
                        urlObj[i].unlockurl = alink['href']
                        i = i + 1
                for alink in tr.findAll('a', {'class':'btn btn-xs bs-tooltip modal-myurl'}):
                    #if alink['src'].find('done') != -1:
                    if alink['href'].find('done') != -1:
                        #doneurl.append(alink['src'])
                        doneurl.append(alink['href'])
                        #urlObj[j].doneurl = alink['src']
                        urlObj[j].doneurl = alink['href']
                        j = j + 1

    urlObj = urlObj[:i]
    print 'urlObj.doneurl: vvvv'
    for x in range(len(urlObj)):
        print urlObj[x].doneurl

    return urlObj




def pushDoneButton(apihost):
    threading.Timer(5.0, pushDoneButton, [apihost]).start()

    url = 'http://' + apihost + '/api/list/paid' #http://localhost:3000/api/list/paid
    try:
        res = rs.get(url)
    except requests.exceptions.RequestException as e:
        print '\nERROR: brain API error: ' + str(e)
        return

    jsontext = res.json()
    for c in jsontext['content']:
        boid = c['boid']

        pushbtnlimit.update({'_id':boid},{'$setOnInsert':{'ctn':1}}, upsert=True)

        payload = {'p_fee':"",'note':"",'id':boid}
        try:
            doc = pushbtnlimit.find_one({"_id":boid})
            if doc != None:
                if doc['ctn'] > 0:
                    print '\n[pushDoneButton] boid: ' + str(boid) + ' push button ' + str(doc['ctn']) + ' times'
                    url = hostname + '/MemberwithdawfundOp/index/setdone'
                    res = rs.post(url, data=payload)
                    pushbtnlimit.update({'_id':boid},{'$inc':{'ctn':-1}})
                else:
                    #print '\n[pushDoneButton] boid: ' + str(boid) + ' do nothing'
                    continue

            #if res.status_code == 200:
                #print '\n boid ' + boid + ' has paid, push done button!\n'
            #else:
                #print '\n boid ' + boid + ' status code != 200.\n'
        except requests.exceptions.RequestException as e:
            errmsg = 'ERROR: post setdone button error: ' + str(e)
            print errmsg
            continue

def penddingFunc():
    threading.Timer(2.0, penddingFunc).start()
    url = 'http://' + apihost + '/api/list/padding'
    try:
        res = rs.get(url)
    except requests.exceptions.RequestException as e:
        print '\nERROR: pendding brain API error: ' + str(e)
        return

    jsontext = res.json()
    for c in jsontext['content']:
        boid = c['boid']

        if boid not in pendingdict:
            pendingdict[boid] = 2

        try:
            if pendingdict[boid] > 0:
                url = hostname + '/MemberwithdawfundOp/index/done/' + boid
                res = rs.get(url)
                pendingdict[boid] -= 1
                #print '[penddingFunc] ' + boid + ' after get done url, lock!'
            else:
                continue
        except requests.exceptions.RequestException as e:
            errmsg = 'ERROR: padding done url error: ' + str(e)
            print errmsg
            continue


class Usage(Exception):
    def __init__(self, msg, exmsg):
        self.msg = msg
        print '\nUsage:\n'
        print msg
        print exmsg
        sys.exit(0)


class Sample:
    name = ''
    average = 0.0
    values = None # list cannot be initialized here!

class UrlCollect:
    doneurl = ''
    unlockurl = ''




# Check have cancel button, if data not exist, delete boid from mongo
# Check manaul paid?
def checkpaid():
    checkword = None
    for row in crawler.find():
        boid = row['boid']
        url = hostname + '/MemberwithdawfundOp/index/cancel/' + boid
        print url
        try:
            res = rs.get(url)
        except requests.exceptions.RequestException as e:
            print "ERROR: check boid " + str(boid) + "paid status error: " + str(e)

        response_text = res.text #check return text
        soup = BeautifulSoup(response_text, "lxml")
        for word in soup.findAll('div', {'class':'modal-body'}):
            try:
                checkword = word.text.strip()
                print 'after cancel button:'
                print checkword

            except:
                checkword = ""
                errmsg = 'ERROR: checkword fail, word.text.strip()'
                print errmsg
                logger.error(errmsg)
                continue

        if checkword != None:
            print '-1?'
            print checkword.find(u"资料不存在或已处理")
            if checkword.find(u"资料不存在或已处理") != -1:
                crawler.remove({"boid":boid})
                histories.insert({"boid":boid,"status":"done"})
                errmsg = '\nboid: ' + boid + ' removed from unpaids table, cause it maybe withdraw or cancel.\n'
                print errmsg
                logger.error(errmsg)



if __name__=="__main__":
    version = '2.5'
    captcha_image = 'captcha.png'
    denoise_image = 'denoise.png'
    pass_factor = 100

    if len(sys.argv) <= 6:
        Usage('Please input hostname & username & password & apihost & pagelimit & sleeptime \n', 'EX: python main.py [hostname] [username] [password] [apihost] [pagelimit] [sleeptime]\n')
    else:
        hostname = sys.argv[1]
        user = sys.argv[2]
        pwd = sys.argv[3]
        apihost = sys.argv[4]
        pagelimit = sys.argv[5]
        sleeptime = sys.argv[6]

    url = r"./bankmap.html"
    page = open(url)

    if os.environ.get("DEBUG") is not None:
        DEBUG = int(os.environ.get("DEBUG"))

    if os.environ.get("SAVE") is not None:
        SAVE = int(os.environ.get("SAVE"))

    conn = pymongo.MongoClient('localhost',27017)
    #conn = pymongo.MongoClient('192.168.10.123',27017)
    db = conn.tigerdb
    crawler = db.unpaids
    histories = db.histories
    pushbtnlimit = db.pushbtnlimit

    if DEBUG == 1:
        d = crawlAccountInfo(rs, "")
        if d != None:
            crawler.insert(d)
            print 'DEBUG Save to mongo\n'
        else:
            print 'Info incomplete, nothing save to mongo, abort!'
        sys.exit(0)

    now = datetime.datetime.now()
    starttime = now.strftime("%Y-%m-%d %H:%M:%S")
    msg = starttime + " VERSION: " + version + " " + "******************* Crawler Start! *******************"
    logger.error(msg)

    breakCaptcha(user, pwd)

    while True:
        print '\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
        print '1. ================== Every ' + sleeptime + ' seconds start getting unpaid content...\n'

        while True:
            print '2. ================== Check have cancel button, if data not exist, delete boid from DB.\n'
            checkpaid()   # Check have cancel button, if data not exist, delete boid from mongo

            print '3. ================== Get querylimit API, if have values, continue going on.\n'
            try:
                url = 'http://' + apihost + '/core/querylimit'
                print url
                res = rs.get(url)
            except requests.exceptions.RequestException as e:
                print '\nERROR: querylimit API error: ' + str(e)
                continue
            jsontext = res.json()
            print jsontext
            if len(jsontext['content']) > 0:
                break
            time.sleep(2)

        print '4. ********************** Breakout whileloop, cause querylimit API have values:  ********************** \n'
        print jsontext['content']

        #a = [200000]
        #for moneylimit in a:
        for moneylimit in jsontext['content']:
            print '5. ================== Get doneurl & unlockurl less than moneylimit.\n'
            print '------------Getting moneylimit below: ' + str(moneylimit)
            urlObj = getWithdrawContent(moneylimit)
            print '6. ================== Get paid boid, and push withdraw done button every 5s.\n'
            pushDoneButton(apihost) #按下確認出款按鈕
            print '7. ================== According urlObjs doneurl that less than moneylimit, looking the account info and save to DB.\n'
            save2mongo(crawler, urlObj)

        print '\nwaiting...'
        time.sleep(int(sleeptime))








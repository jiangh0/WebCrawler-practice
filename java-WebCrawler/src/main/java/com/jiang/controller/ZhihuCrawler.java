package com.jiang.controller;

import java.io.DataInputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.List;

import org.apache.log4j.Logger;

import com.gargoylesoftware.htmlunit.BrowserVersion;
import com.gargoylesoftware.htmlunit.FailingHttpStatusCodeException;
import com.gargoylesoftware.htmlunit.WebClient;
import com.gargoylesoftware.htmlunit.html.DomElement;
import com.gargoylesoftware.htmlunit.html.HtmlPage;
import com.jiang.util.StringUtil;

/**
 * 知乎网站爬虫
 * @author JH
 *
 */
public class ZhihuCrawler {
	
	private static Logger logger = Logger.getLogger(ZhihuCrawler.class);

	/**
	 * 爬取某个问题下所有所有回答包含的图片
	 */
	public static void getAnswerPicture() {
		WebClient webClient = new WebClient(BrowserVersion.CHROME);
		webClient.getOptions().setCssEnabled(false);
		webClient.getOptions().setJavaScriptEnabled(false);
		try{
			//解析获取页面
			HtmlPage page = webClient.getPage("https://www.zhihu.com/question/40778754");
			String title = page.getElementsByTagName("title").get(0).getTextContent();
			//创建知乎某知乎的特定文件夹
			File dir = new File("e:\\WebCrawler/zhihu/" + title);
			if(!dir.exists())
				dir.mkdirs();
			//保存知乎某问题网页源代码
			File xml = new File(dir.getPath() + "/html.txt" );
			FileOutputStream os = new FileOutputStream(xml);
			os.write(page.asXml().getBytes());
			os.close();
			List<DomElement> imgs = page.getElementsByTagName("noscript");
			for(DomElement img : imgs){
				img = (DomElement) img.getElementsByTagName("img").get(0);
				URL url = null;
				if(StringUtil.isNotEmpty(img.getAttribute("data-original"))) {
					url = new URL(img.getAttribute("data-original"));
				}else {
					url = new URL(img.getAttribute("src"));
				}
	            // 打开网络输入流
	            DataInputStream dis = new DataInputStream(url.openStream());
	            File file = new File(dir.getPath()+ "/" + System.currentTimeMillis() + ".jpg");
	            // 建立一个新的文件
	            FileOutputStream fos = new FileOutputStream(file);
	            byte[] buffer = new byte[1024];
	            int length;
	            // 开始填充数据
	            while ((length = dis.read(buffer)) > 0) {
	                fos.write(buffer, 0, length);
	            }
	            dis.close();
	            fos.close();
	            logger.info("ok");
			}
		} catch (FailingHttpStatusCodeException e) {
			e.printStackTrace();
			logger.error("解析网页报错", e);
		} catch (MalformedURLException e) {
			e.printStackTrace();
			logger.error("解析网页报错", e);
		} catch (IOException e) {
			e.printStackTrace();
			logger.error("解析网页报错", e);
		}
	}
	
	
	public static void main(String[] args) {
		getAnswerPicture();
	}
}

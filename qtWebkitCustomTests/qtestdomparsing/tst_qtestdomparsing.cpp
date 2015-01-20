#include <QtTest/QtTest>
#include <QAction>

#include "qwebframe.h"
#include "qwebview.h"
#include "qdebug.h"
#include "qwebelement.h"

class tst_qtestdomparsing : public QObject
{
    Q_OBJECT

public:
    tst_qtestdomparsing();
    virtual ~tst_qtestdomparsing();
    void examineChildElements(QWebElement parentElement)
    {
        QWebElement element = parentElement.firstChild();
           while (!element.isNull()) {

               examineChildElements(element);
               element = element.nextSibling();
           }
           QCOMPARE(element.tagName(),QString(""));
    }


public slots:
    void init();
    void cleanup();

private slots:
    void domFunctDocumentElement();
    void domFunctFirstChild();
    void domFunctEvaluateJS();
    void domFunctEmptyUrl();

private:
    QWebView* m_view;
};

tst_qtestdomparsing::tst_qtestdomparsing()
{
}

tst_qtestdomparsing::~tst_qtestdomparsing()
{
}

void tst_qtestdomparsing::init()
{
    m_view = new QWebView;
    m_view->load(QUrl("http://camendesign.com/code/video_for_everybody/test.html"));
}

void tst_qtestdomparsing::cleanup()
{
    //delete page;
}

/**
  * Check QFrame::documentElement() method
  */
void tst_qtestdomparsing::domFunctDocumentElement()
{
    QWebFrame *frame = m_view->page()->mainFrame();
    QWebElement document = frame->documentElement();

    QCOMPARE(document.tagName(),QString("HTML"));
}

/**
  * Check QWebElement::firstChild() method
  */
void tst_qtestdomparsing::domFunctFirstChild()
{
    QWebFrame *frame = m_view->page()->mainFrame();
    QWebElement document = frame->documentElement();

    QWebElement firstChild = document.firstChild();
    QCOMPARE(firstChild.tagName(),QString("HEAD"));

}

/**
  * Check QWebElement::evaluateJavascript() method
  */
void tst_qtestdomparsing::domFunctEvaluateJS()
{
    m_view->setHtml("<html><head><title>EvaluateJs on a QWebFrame</title><h1>Hello World</head></head><body bgcolor='cyan'><canvas id='mycanvas' width='640' height='480' style=''></canvas></body></html>");
    QWebFrame *frame = m_view->page()->mainFrame();

    frame->addToJavaScriptWindowObject("document",frame);

    QWebElement documentElement = frame->documentElement();
    QVariant result = documentElement.evaluateJavaScript("this.tagName");

    QVERIFY(result.isValid());
    QVERIFY(result.type() == QVariant::String);
    QCOMPARE(result.toString(), QLatin1String("HTML"));

}

/**************
 *The tag name should be empty when we try to parse the webpage
 *as the url is empty
 *******/
void tst_qtestdomparsing::domFunctEmptyUrl()
{
    QUrl url = QUrl("");
    m_view->load(url);

    QVERIFY2(url.isEmpty(),"Failure");
    QWebFrame *frame = m_view->page()->mainFrame();
    QWebElement documentElement = frame->documentElement();

    examineChildElements(documentElement);
}


QTEST_MAIN(tst_qtestdomparsing)
#include "tst_qtestdomparsing.moc"


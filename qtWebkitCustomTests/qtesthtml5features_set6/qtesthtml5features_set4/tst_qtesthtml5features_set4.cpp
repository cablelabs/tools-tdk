#include <QString>
#include <QtTest>
#include <QWebView>
#include <QWebFrame>
#include "../util.h"
class tst_qtesthtml5features_set4 : public QObject
{
    Q_OBJECT
    
public:
    tst_qtesthtml5features_set4();
    
private Q_SLOTS:
    void htmlFunctLoadedMetaData();
    void htmlFunctWindowOnload();
    void htmlFunctImageOnload();
    void htmlFunctScriptOnload();
    void htmlFunctIframeOnload();
    void htmlFunctLineJoin();
    void htmlFunctReadyState();
    void htmlFunctSpellCheck();
    void htmlFunctHiddenAttribute();
    void htmlFunctStrokeStyle();
    void htmlFunctProgress();
    void htmlFunctTextAlign();
    void htmlFunctLineCap();
    void htmlFunctAbort();
    void htmlFunctBuffered();
    void htmlFunctVideoCanplay();
    void htmlFunctLoadedData();


private:
    QWebView* m_view;
    QTimer *timer;
    QVariant resultLoadedMetaData;
    QVariant resultBufferedProp;
    QVariant resultIframeOnload;
    QVariant resultGetVideoReadyState;
    QVariant resultCanplay;
    QVariant resultLoadedData;

public slots:

    void slotLoadedMetadata();
    void slotBufferedProp();
    void slotIframeOnload();
    void slotGetVideoReadyState();
    void slotCanplayVideo();
    void slotLoadedData();

};

tst_qtesthtml5features_set4::tst_qtesthtml5features_set4()
{
}



/*******************
 *Loads a web page with
 *HTML5 loadedmetadata
 *****************/
void tst_qtesthtml5features_set4::htmlFunctLoadedMetaData()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/loadedMetaData.html"));
    m_view->show();
    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));
    timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(slotLoadedMetadata()));
    timer->start(1000);
    QVERIFY(::waitForSignal(timer,SIGNAL(destroyed())));
    QVERIFY(resultLoadedMetaData.toBool());
}

void tst_qtesthtml5features_set4::slotLoadedMetadata()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("loadEvent()");
    qDebug() << "slotLoadedMetadata Getting the result" << result.toString();
    if(result.toBool() == false)
    {
        qDebug() << "Continue polling";
    }
    else
    {
        qDebug() << "Getting the result" << result.toString();
        qDebug()<< "Stop the timer";
        resultLoadedMetaData=result.toString();
        timer->stop();
        timer->deleteLater();
    }
}
/*******************
 *Loads a web page with
 *HTML5 window.onload
 *****************/
void tst_qtesthtml5features_set4::htmlFunctWindowOnload()
{
    QWebView *m_view = new QWebView;

    QFile file(":/resources/windowOnload.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("windowLoad()");
    qDebug() << "Getting the result "<< result.toString();
    QVERIFY2(result.toBool(),"Failure");
}

/*******************
 *Loads a web page with
 *HTML5 img.onload
 *****************/
void tst_qtesthtml5features_set4::htmlFunctImageOnload()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/imageOnload.html"));
    m_view->show();
    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("imageLoad()");
    qDebug() << "Getting the result "<< result.toString();
    QVERIFY2(result.toBool(),"Failure");
}

/*******************
 *Loads a web page with
 *HTML5 script.onload
 *****************/
void tst_qtesthtml5features_set4::htmlFunctScriptOnload()
{
    QWebView *m_view = new QWebView;

    QFile file(":/resources/scriptOnload.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("scriptOnload()");
    qDebug() << "Getting the result "<< result.toString();
    QVERIFY2(result.toBool(),"Failure");
}

/*******************
 *Loads a web page with
 *HTML5 iframe.onload
 *****************/

void tst_qtesthtml5features_set4::htmlFunctIframeOnload()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/iframeOnload.html"));
    m_view->show();
    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));
    timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(slotIframeOnload()));
    timer->start(1000);
    QVERIFY(::waitForSignal(timer,SIGNAL(destroyed())));
    QVERIFY(resultIframeOnload.toBool());
}

void tst_qtesthtml5features_set4::slotIframeOnload()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("frameOnload()");
    qDebug() << "slotIframeOnload Getting the result" << result.toString();
    if(result.toBool() == false)
    {
        qDebug() << "Continue polling";
    }
    else
    {
        qDebug() << "Getting the result" << result.toString();
        qDebug()<< "Stop the timer";
        resultIframeOnload=result.toString();
        timer->stop();
        timer->deleteLater();
    }
}
/*******************
 *Loads a web page with
 *HTML5 canvas linejoin
 *****************/
void tst_qtesthtml5features_set4::htmlFunctLineJoin()
{
    QWebView *m_view = new QWebView;

    QFile file(":/resources/lineJoin.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("joinLine()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(QString(result.toString()),QString("round"));

}

/*******************
 *Loads a web page with
 *HTML5 document readystate
 *****************/

void tst_qtesthtml5features_set4::htmlFunctReadyState()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/readyState.html"));
    m_view->show();
    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));
    timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(slotGetVideoReadyState()));
    timer->start(1000);
    QVERIFY(::waitForSignal(timer,SIGNAL(destroyed())));
    QVERIFY(resultGetVideoReadyState.toBool());
}

void tst_qtesthtml5features_set4::slotGetVideoReadyState()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("myReadyState()");
    qDebug() << "slotGetVideoReadyState Getting the result" << result.toString();
    if(result.toBool() == false)
    {
        qDebug() << "Continue polling";
    }
    else
    {
        qDebug() << "Getting the result" << result.toString();
        qDebug()<< "Stop the timer";
        resultGetVideoReadyState=result.toString();
        timer->stop();
        timer->deleteLater();
    }
}

/*******************
 *Loads a web page with
 *HTML5 spellcheck
 *****************/
void tst_qtesthtml5features_set4::htmlFunctSpellCheck()
{
    QWebView *m_view = new QWebView;

    QFile file(":/resources/spellCheck.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("spellCheck()");
    qDebug() << "Getting the result "<< result.toString();    
    QVERIFY2(result.toBool(),"Failure");

}

/*******************
 *Loads a web page with
 *HTML5 hidden attribute
 *****************/
void tst_qtesthtml5features_set4::htmlFunctHiddenAttribute()
{
    QWebView *m_view = new QWebView;

    QFile file(":/resources/hidden.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("hiddenAttr()");
    qDebug() << "Getting the result "<< result.toString();    
    QVERIFY2(result.toBool(),"Failure");

}

/*******************
 *Loads a web page with
 *HTML5 canvas strokestyle 
 *****************/

void tst_qtesthtml5features_set4::htmlFunctStrokeStyle()
{
    QWebView *m_view = new QWebView;

    QFile file(":/resources/strokeStyle.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("strokeStyle()");
    qDebug() << "Getting the result "<< result.toString();    
    QCOMPARE(QString(result.toString()),QString("#ff0000"));
}

/*******************
 *Loads a web page with
 *HTML5 progress bar
 *****************/
void tst_qtesthtml5features_set4::htmlFunctProgress()
{
    QWebView *m_view = new QWebView;

    QFile file(":/resources/progress.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("progressBar()");
    qDebug() << "Getting the result "<< result.toString();    
    QVERIFY2(result.toBool(),"Failure");

}

/*******************
 *Loads a web page with
 *HTML5 textAlign
 *****************/
void tst_qtesthtml5features_set4::htmlFunctTextAlign()
{
    QWebView *m_view = new QWebView;

    QFile file(":/resources/textAlign.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("txtAlign()");
    qDebug() << "Getting the result "<< result.toString();    
    QCOMPARE(QString(result.toString()),QString("center"));
}

/*******************
 *Loads a web page with
 *HTML5 canvas linecap
 *****************/
void tst_qtesthtml5features_set4::htmlFunctLineCap()
{
    QWebView *m_view = new QWebView;

    QFile file(":/resources/lineCap.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("canvasLineCap()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(QString(result.toString()),QString("round"));

}

/*******************
 *Loads a web page with
 *HTML5 window abort
 *****************/
void tst_qtesthtml5features_set4::htmlFunctAbort()
{
    QWebView *m_view = new QWebView;

    QFile file(":/resources/windowOnabort.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("windowAbort()");
    qDebug() << "Getting the result "<< result.toString();
    QVERIFY2(result.toBool(),"Failure");
}

/*******************
 *Loads a web page with
 *HTML5 buffered
 *****************/
void tst_qtesthtml5features_set4::htmlFunctBuffered()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/buffered.html"));
    m_view->show();
    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));
    timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(slotBufferedProp()));
    timer->start(1000);
    QVERIFY(::waitForSignal(timer,SIGNAL(destroyed())));
    QVERIFY(resultBufferedProp.toBool());
}

void tst_qtesthtml5features_set4::slotBufferedProp()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("getBuffRange()");
    qDebug() << "slotBufferedProp Getting the result" << result.toString();
    if(result.toBool() == false)
    {
        qDebug() << "Continue polling";
    }
    else
    {
        qDebug() << "Getting the result" << result.toString();
        qDebug()<< "Stop the timer";
        resultBufferedProp=result.toString();
        timer->stop();
        timer->deleteLater();
    }
}

/*******************
 *Loads a web page with
 *HTML5 canplay
 *****************/
void tst_qtesthtml5features_set4::htmlFunctVideoCanplay()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/canplayVideo.html"));
    m_view->show();
    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));
    timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(slotCanplayVideo()));
    timer->start(1000);
    QVERIFY(::waitForSignal(timer,SIGNAL(destroyed())));
    QVERIFY(resultCanplay.toBool());
}

void tst_qtesthtml5features_set4::slotCanplayVideo()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("canplayEvent()");
    qDebug() << "slotCanplayVideo Getting the result" << result.toString();
    if(result.toBool() == false)
    {
        qDebug() << "Continue polling";
    }
    else
    {
        qDebug() << "Getting the result" << result.toString();
        qDebug()<< "Stop the timer";
        resultCanplay=result.toString();
        timer->stop();
        timer->deleteLater();
    }
}
/*******************
 *Loads a web page with
 *HTML5 loadedmetadata
 *****************/
void tst_qtesthtml5features_set4::htmlFunctLoadedData()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/loadedData.html"));
    m_view->show();
    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));
    timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(slotLoadedData()));
    timer->start(1000);
    QVERIFY(::waitForSignal(timer,SIGNAL(destroyed())));
    QVERIFY(resultLoadedData.toBool());
}

void tst_qtesthtml5features_set4::slotLoadedData()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("getLoadedEvent()");
    qDebug() << "slotLoadedData Getting the result" << result.toString();
    if(result.toBool() == false)
    {
        qDebug() << "Continue polling";
    }
    else
    {
        qDebug() << "Getting the result" << result.toString();
        qDebug()<< "Stop the timer";
        resultLoadedData=result.toString();
        timer->stop();
        timer->deleteLater();
    }
}

QTEST_MAIN(tst_qtesthtml5features_set4)

#include "tst_qtesthtml5features_set4.moc"

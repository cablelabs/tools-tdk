#include <QString>
#include <QtTest>
#include <QWebView>
#include <QWebFrame>
#include "../util.h"

class tst_qtesthtml5features_set6 : public QObject
{
    Q_OBJECT
    
public:
    tst_qtesthtml5features_set6();
    
private Q_SLOTS:
    void htmlFunctBodyOnload();
    void htmlFunctFramesetOnload();		
    void htmlFunctStyleOnload();
    void htmlFunctLinkOnload();
    void htmlFunctWindowOnunload();
    void htmlFunctContentEditable();
    void htmlFunctSeekable();
    void htmlFunctDefaultPlaybackRate();
    void htmlFunctTabIndex();
    void htmlFunctStyle();
    void htmlFunctSeeking();
    void htmlFunctSuspend();
    void htmlFunctVideoWaiting();
    void htmlFunctLang();
    void htmlFunctTitle();

private:
    QWebView* m_view;
    QTimer *timer;
    QVariant resultframesetOnload;
    QVariant resultlinkOnload;
    QVariant resultSeekable;
    QVariant resultDefaultPlaybackRate;
    QVariant resultSeeking;
    QVariant resultSuspend;
    QVariant resultVideoWaiting;

public slots:

    void slotframesetOnload();
    void slotlinkOnload();
    void slotSeekable();
    void slotDefaultPlaybackRate();
    void slotSeeking();
    void slotSuspend();
    void slotVideoWaiting();
};

tst_qtesthtml5features_set6::tst_qtesthtml5features_set6()
{
}

/*******************
 *Loads a web page with
 *HTML5 body.onload
 *****************/
void tst_qtesthtml5features_set6::htmlFunctBodyOnload()
{
    m_view = new QWebView;

    QFile file(":/resources/bodyOnload.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifyBodyOnload()");
    qDebug() << "Getting the result "<< result.toString();
    QVERIFY2(result.toBool(),"Failure");
}

/*******************
 *Loads a web page with
 *HTML5 frameset.onload
 *****************/

void tst_qtesthtml5features_set6::htmlFunctFramesetOnload()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/framesetOnload.html"));
    // m_view->show();
    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));
    timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(slotframesetOnload()));
    timer->start(1000);
    QVERIFY(::waitForSignal(timer,SIGNAL(destroyed())));
    QVERIFY(resultframesetOnload.toBool());
}

void tst_qtesthtml5features_set6::slotframesetOnload()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("framesetOnload()");
    qDebug() << "slotframesetOnload Getting the result" << result.toString();
    if(result.toBool() == false)
    {
        qDebug() << "Continue polling";
    }
    else
    {
        qDebug() << "Getting the result" << result.toString();
        qDebug()<< "Stop the timer";
        resultframesetOnload=result.toString();
        timer->stop();
        timer->deleteLater();
    }
}

/*******************
 *Loads a web page with
 *HTML5 style.onload
 *****************/
void tst_qtesthtml5features_set6::htmlFunctStyleOnload()
{
    m_view = new QWebView;

    QFile file(":/resources/styleOnload.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifyStyleOnload()");
    qDebug() << "Getting the result "<< result.toString();
    QVERIFY2(result.toBool(),"Failure");
}

/*******************
 *Loads a web page with
 *HTML5 link.onload
 *****************/
void tst_qtesthtml5features_set6::htmlFunctLinkOnload()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/linkOnload.html"));
    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));
    timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(slotlinkOnload()));
    timer->start(1000);
    QVERIFY(::waitForSignal(timer,SIGNAL(destroyed())));
    QVERIFY(resultlinkOnload.toBool());
}

void tst_qtesthtml5features_set6::slotlinkOnload()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifyLinkLoaded()");
    qDebug() << "slotlinkOnload Getting the result" << result.toString();
    if(result.toBool() == false)
    {
        qDebug() << "Continue polling";
    }
    else
    {
        qDebug() << "Getting the result" << result.toString();
        qDebug()<< "Stop the timer";
        resultlinkOnload=result.toString();
        timer->stop();
        timer->deleteLater();
    }
}

/*******************
 *Loads a web page with
 *HTML5 windowOnunload
 *****************/
void tst_qtesthtml5features_set6::htmlFunctWindowOnunload()
{
    m_view = new QWebView;

    QFile file(":/resources/windowOnunload.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifyTest()");
    qDebug() << "Getting the result "<< result.toString();
    QVERIFY2(result.toBool(),"Failure");
}

/*******************
 *Loads a web page with
 *HTML5 contenteditable
 *****************/
void tst_qtesthtml5features_set6::htmlFunctContentEditable()
{
    m_view = new QWebView;

    QFile file(":/resources/htmlContentEditable.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifyTest()");
    qDebug() << "Getting the result "<< result.toString();
    QVERIFY2(result.toBool(),"Failure");
}

/*******************
 *Loads a web page with
 *HTML5 event seekable
 *****************/
void tst_qtesthtml5features_set6::htmlFunctSeekable()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/htmlSeekable.html"));
    //m_view->show();
    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));
    timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(slotSeekable()));
    timer->start(1000);
    QVERIFY(::waitForSignal(timer,SIGNAL(destroyed())));
    QVERIFY(resultSeekable.toBool());
}

void tst_qtesthtml5features_set6::slotSeekable()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifySeekable()");
    qDebug() << "slotSeekable Getting the result" << result.toString();
    if(result.toBool() == false)
    {
        qDebug() << "Continue polling";
    }
    else
    {
        qDebug() << "Getting the result" << result.toString();
        qDebug()<< "Stop the timer";
        resultSeekable=result.toString();
        timer->stop();
        timer->deleteLater();
    }
}

/*******************
 *Loads a web page with
 *HTML5 defaultPlaybackRate
 *****************/
void tst_qtesthtml5features_set6::htmlFunctDefaultPlaybackRate()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/htmlDefaultPlaybackRate.html"));
    // m_view->show();
    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));
    timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(slotDefaultPlaybackRate()));
    timer->start(1000);
    QVERIFY(::waitForSignal(timer,SIGNAL(destroyed())));
    QVERIFY(resultDefaultPlaybackRate.toBool());
}

void tst_qtesthtml5features_set6::slotDefaultPlaybackRate()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifyTest()");
    qDebug() << "slotDefaultPlaybackRate Getting the result" << result.toString();
    if(result.toBool() == false)
    {
        qDebug() << "Continue polling";
    }
    else
    {
        qDebug() << "Getting the result" << result.toString();
        qDebug()<< "Stop the timer";
        resultDefaultPlaybackRate=result.toString();
        timer->stop();
        timer->deleteLater();
    }
}

/*******************
 *Loads a web page with
 *HTML5 TabIndex
 *****************/
void tst_qtesthtml5features_set6::htmlFunctTabIndex()
{
    m_view = new QWebView;

    QFile file(":/resources/tabindex.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifyTabIndex()");
    qDebug() << "Getting the result "<< result.toString();
    QVERIFY2(result.toBool(),"Failure");
}

/*******************
 *Loads a web page with
 *HTML5 style
 *****************/
void tst_qtesthtml5features_set6::htmlFunctStyle()
{
    m_view = new QWebView;
    QFile file(":/resources/style.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifyTestStyle()");
    qDebug() << "Getting the result "<< result.toString();
    QVERIFY2(result.toBool(),"Failure");
}


/*******************
 *Loads a web page with
 *HTML5 seeking
 *****************/
void tst_qtesthtml5features_set6::htmlFunctSeeking()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/seeking.html"));
    // m_view->show();
    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));
    timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(slotSeeking()));
    timer->start(1000);
    QVERIFY(::waitForSignal(timer,SIGNAL(destroyed())));
    QVERIFY(resultSeeking.toBool());
}

void tst_qtesthtml5features_set6::slotSeeking()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifySeekingTest()");
    qDebug() << "slotSeeking Getting the result" << result.toString();
    if(result.toBool() == false)
    {
        qDebug() << "Continue polling";
    }
    else
    {
        qDebug() << "Getting the result" << result.toString();
        qDebug()<< "Stop the timer";
        resultSeeking=result.toString();
        timer->stop();
        timer->deleteLater();
    }
}

void tst_qtesthtml5features_set6::htmlFunctVideoWaiting()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/videoWaiting.html"));
    //m_view->show();
    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));
    timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(slotVideoWaiting()));
    timer->start(1000);
    QVERIFY(::waitForSignal(timer,SIGNAL(destroyed())));
    QVERIFY(resultVideoWaiting.toBool());
}

void tst_qtesthtml5features_set6::slotVideoWaiting()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("waitEvent()");
    qDebug() << "slotVideoWaiting Getting the result" << result.toString();
    if(result.toBool() == false)
    {
        qDebug() << "Continue polling";
    }
    else
    {
        qDebug() << "Getting the result" << result.toString();
        qDebug()<< "Stop the timer";
        resultVideoWaiting=result.toString();
        timer->stop();
        timer->deleteLater();
    }
}


/*******************
 *Loads a web page with
 *HTML5 suspend
 *****************/
void tst_qtesthtml5features_set6::htmlFunctSuspend()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/htmlSuspend.html"));
    //m_view->show();
    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));
    timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(slotSuspend()));
    timer->start(1000);
    QVERIFY(::waitForSignal(timer,SIGNAL(destroyed())));
    QVERIFY(resultSuspend.toBool());
}

void tst_qtesthtml5features_set6::slotSuspend()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifySuspended()");
    qDebug() << "slotSuspend Getting the result" << result.toString();
    if(result.toBool() == false)
    {
        qDebug() << "Continue polling";
    }
    else
    {
        qDebug() << "Getting the result" << result.toString();
        qDebug()<< "Stop the timer";
        resultSuspend=result.toString();
        timer->stop();
        timer->deleteLater();
    }
}

/*******************
 *Loads a web page with
 *HTML5 Lang
 *****************/
void tst_qtesthtml5features_set6::htmlFunctLang()
{
    m_view = new QWebView;

    QFile file(":/resources/htmlLang.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifyLang()");
    qDebug() << "Getting the result "<< result.toString();
    QVERIFY2(result.toBool(),"Failure");
}

/*******************
 *Loads a web page with
 *HTML5 Title
 *****************/
void tst_qtesthtml5features_set6::htmlFunctTitle()
{
    m_view = new QWebView;

    QFile file(":/resources/htmlTitle.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifyTitle()");
    qDebug() << "Getting the result "<< result.toString();
    QVERIFY2(result.toBool(),"Failure");
}

QTEST_MAIN(tst_qtesthtml5features_set6)

#include "tst_qtesthtml5features_set6.moc"

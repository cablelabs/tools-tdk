#include <QString>
#include <QtTest>
#include <QWebView>
#include <QWebFrame>
#include "../util.h"
class tst_qtesthtml5features_set5 : public QObject
{
    Q_OBJECT
    
public:
    tst_qtesthtml5features_set5();
    
private Q_SLOTS:
    void htmlFunctEmptied();
    void htmlFunctVideoCanplayThru();
    void htmlFunctLineWidth();
    void htmlFunctWebSocketOnmessage();
    void htmlFunctMiterLimit();
    void htmlFunctScriptOnerror();
    void htmlFunctImageOnerror();
    void htmlFunctWindowOnerror();
    void htmlFunctVideoRateChange();
    void htmlFunctDraggableAttr();
    void htmlFunctVideoTimeUpdate();
    void htmlFunctVideoPlayedRange();
    void htmlFunctDataExtendedAttribute();
    void htmlFunctCanvasImageData();


private:
    QWebView* m_view;
    QTimer *timer;
    QVariant resultEmptyEvent;
    QVariant resultCanplayThru;
    QVariant resultOnMessage;
    QVariant resultVideoRateChange;
    QVariant resultVideoTimeUpdate;
    QVariant resultVideoPlayedRange;

public slots:

    void slotEmptyEvent();
    void slotCanplayThruVideo();
    void slotWebSocketOnmessage();
    void slotVideoRateChange();
    void slotVideoTimeUpdate();
    void slotVideoPlayedRange();

};

tst_qtesthtml5features_set5::tst_qtesthtml5features_set5()
{
}

void tst_qtesthtml5features_set5::htmlFunctEmptied()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/emptied.html"));

    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("invokeEmptyEvnt()");
    qDebug() << "invokeEmptyEvnt Getting the result" << result.toString();

    timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(slotEmptyEvent()));
    timer->start(1000);
    QVERIFY(::waitForSignal(timer,SIGNAL(destroyed())));
    QVERIFY(resultEmptyEvent.toBool());
}
void tst_qtesthtml5features_set5::slotEmptyEvent()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("checkEmptyEvent()");
    qDebug() << "slotEmptyEvent Getting the result" << result.toString();
    if(result.toBool() == false)
    {
        qDebug() << "Continue polling";
    }
    else
    {
        qDebug() << "Getting the result" << result.toString();
        qDebug()<< "Stop the timer";
        resultEmptyEvent=result.toString();
        timer->stop();
        timer->deleteLater();
    }
}
/*******************
 *Loads a web page with
 *HTML5 canplaythru
 *****************/
void tst_qtesthtml5features_set5::htmlFunctVideoCanplayThru()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/canplayThruVideo.html"));
    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));
    timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(slotCanplayThruVideo()));
    timer->start(1000);
    QVERIFY(::waitForSignal(timer,SIGNAL(destroyed())));
    QVERIFY(resultCanplayThru.toBool());
}

void tst_qtesthtml5features_set5::slotCanplayThruVideo()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("canplayThruEvent()");
    qDebug() << "slotCanplayThruVideo Getting the result" << result.toString();
    if(result.toBool() == false)
    {
        qDebug() << "Continue polling";
    }
    else
    {
        qDebug() << "Getting the result" << result.toString();
        qDebug()<< "Stop the timer";
        resultCanplayThru=result.toString();
        timer->stop();
        timer->deleteLater();
    }
}

/*******************
 *Loads a web page with
 *HTML5 canvas linewidth
 *****************/
void tst_qtesthtml5features_set5::htmlFunctLineWidth()
{
    m_view = new QWebView;

    QFile file(":/resources/lineWidth.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("canvasLineWidth()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(QString(result.toString()),QString("10"));

}

/*******************
 *Loads a web page with
 *HTML5 websocket.onmessage
 *****************/

void tst_qtesthtml5features_set5::htmlFunctWebSocketOnmessage()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/onMessage.html"));
    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));
    timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(slotWebSocketOnmessage()));
    timer->start(1000);
    QVERIFY(::waitForSignal(timer,SIGNAL(destroyed())));
    QVERIFY(resultOnMessage.toBool());
}

void tst_qtesthtml5features_set5::slotWebSocketOnmessage()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("checkMessage()");
    qDebug() << "slotWebSocketOnmessage Getting the result" << result.toString();
    if(result.toBool() == false)
    {
        qDebug() << "Continue polling";
    }
    else
    {
        qDebug() << "Getting the result" << result.toString();
        qDebug()<< "Stop the timer";
        resultOnMessage=result.toString();
        timer->stop();
        timer->deleteLater();
    }
}

/*******************
 *Loads a web page with
 *HTML5 canvas miterlimit
 *****************/
void tst_qtesthtml5features_set5::htmlFunctMiterLimit()
{
    m_view = new QWebView;

    QFile file(":/resources/miterLimit.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("canvasMiterLimit()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(QString(result.toString()),QString("5"));

}

/*******************
 *Loads a web page with
 *HTML5 script onerror
 *****************/
void tst_qtesthtml5features_set5::htmlFunctScriptOnerror()
{
    m_view = new QWebView;

    QFile file(":/resources/scriptOnerror.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("scriptError()");
    qDebug() << "Getting the result "<< result.toString();
    QVERIFY2(result.toBool(),"Failure");

}

/*******************
 *Loads a web page with
 *HTML5 image onerror
 *****************/
void tst_qtesthtml5features_set5::htmlFunctImageOnerror()
{
    m_view = new QWebView;

    QFile file(":/resources/imageOnerror.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("imageError()");
    qDebug() << "Getting the result "<< result.toString();
    QVERIFY2(result.toBool(),"Failure");

}

/*******************
 *Loads a web page with
 *HTML5 image onerror
 *****************/
void tst_qtesthtml5features_set5::htmlFunctWindowOnerror()
{
    m_view = new QWebView;

    QFile file(":/resources/windowOnerror.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("windowError()");
    qDebug() << "Getting the result "<< result.toString();
    QVERIFY2(result.toBool(),"Failure");

}
/*******************
 *Loads a web page with
 *HTML5 ratechange
 *****************/

void tst_qtesthtml5features_set5::htmlFunctVideoRateChange()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/videoRateChange.html"));

    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));
    timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(slotVideoRateChange()));
    timer->start(1000);
    QVERIFY(::waitForSignal(timer,SIGNAL(destroyed())));
    QVERIFY(resultVideoRateChange.toBool());
}

void tst_qtesthtml5features_set5::slotVideoRateChange()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("rateChangeEvent()");
    qDebug() << "slotVideoRateChange Getting the result" << result.toString();
    if(result.toBool() == false)
    {
        qDebug() << "Continue polling";
    }
    else
    {
        qDebug() << "Getting the result" << result.toString();
        qDebug()<< "Stop the timer";
        resultVideoRateChange=result.toString();
        timer->stop();
        timer->deleteLater();
    }
}

/*******************
 *Loads a web page with
 *HTML5 draggable
 *****************/
void tst_qtesthtml5features_set5::htmlFunctDraggableAttr()
{
    m_view = new QWebView;

    QFile file(":/resources/draggable.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("dragFunct()");
    qDebug() << "Getting the result "<< result.toString();
    QVERIFY2(result.toBool(),"Failure");

}

/*******************
 *Loads a web page with
 *HTML5 timeupdate
 *****************/

void tst_qtesthtml5features_set5::htmlFunctVideoTimeUpdate()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/timeUpdate.html"));

    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));
    timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(slotVideoTimeUpdate()));
    timer->start(1000);
    QVERIFY(::waitForSignal(timer,SIGNAL(destroyed())));
    QVERIFY(resultVideoTimeUpdate.toBool());
}

void tst_qtesthtml5features_set5::slotVideoTimeUpdate()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("updatedTime()");
    qDebug() << "slotVideoTimeUpdate Getting the result" << result.toString();
    if(result.toBool() == false)
    {
        qDebug() << "Continue polling";
    }
    else
    {
        qDebug() << "Getting the result" << result.toString();
        qDebug()<< "Stop the timer";
        resultVideoTimeUpdate=result.toString();
        timer->stop();
        timer->deleteLater();
    }
}

/*******************
 *Loads a web page with
 *HTML5 played
 *****************/

void tst_qtesthtml5features_set5::htmlFunctVideoPlayedRange()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/videoPlayed.html"));
    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));
    timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(slotVideoPlayedRange()));
    timer->start(1000);
    QVERIFY(::waitForSignal(timer,SIGNAL(destroyed())));
    QVERIFY(resultVideoPlayedRange.toBool());
}

void tst_qtesthtml5features_set5::slotVideoPlayedRange()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("playedRange()");
    qDebug() << "slotVideoPlayedRange Getting the result" << result.toString();
    if(result.toBool() == false)
    {
        qDebug() << "Continue polling";
    }
    else
    {
        qDebug() << "Getting the result" << result.toString();
        qDebug()<< "Stop the timer";
        resultVideoPlayedRange=result.toString();
        timer->stop();
        timer->deleteLater();
    }
}

/*******************
 *Loads a web page with
 *HTML5 data-* attribute
 *****************/
void tst_qtesthtml5features_set5::htmlFunctDataExtendedAttribute()
{
    m_view = new QWebView;

    QFile file(":/resources/dataExtAttr.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("getDataAttr()");
    qDebug() << "Getting the result "<< result.toString();
    QVERIFY2(result.toBool(),"Failure");

}

/*******************
 *Loads a web page with
 *HTML5 canvas image data
 *****************/
void tst_qtesthtml5features_set5::htmlFunctCanvasImageData()
{
    m_view = new QWebView;

    QFile file(":/resources/canvasData.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("getImgData()");
    qDebug() << "Getting the result "<< result.toString();
    QVERIFY2(result.toBool(),"Failure");

}
QTEST_MAIN(tst_qtesthtml5features_set5)

#include "tst_qtesthtml5features_set5.moc"

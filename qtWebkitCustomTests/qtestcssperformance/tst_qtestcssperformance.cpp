#include <QString>
#include <QtTest>
#include <QWebView>
#include <QProcess>
#include <QWebFrame>
#include "../util.h"
char *s_tdkPath = getenv("TDK_PATH");
class tst_qtestcssperformance : public QObject
{
    Q_OBJECT
    
public:
    tst_qtestcssperformance();
    
private Q_SLOTS:
    void cssPerfmGetMemoryUsed();
    void cssPerfmGetMemoryForAnimation();
    void cssPerfmMemoryUsedFor3dTransform();
    void cssPerfmGetTimeToPlayAnimation();
    void cssPerfmMemoryUsedForBackgroundChange();
    void cssPerfmTimeToLoadCSS2dTranforms();
    void cssPerfmTimeToLoadCSSTranforms();
    void cssPerfmTimeToFinishCSSAnimation();

public slots:
    void slotAnimationStarted();
    void slotLoadedTransforms();
    void slotFinishedAnimation();
    void slotLoaded2dTransforms();

private:
      QWebView * m_view;
      QTimer *pollingtimer;
      int videoLoadTime;
      QTime timer;

};

tst_qtestcssperformance::tst_qtestcssperformance()
{
    m_view = new QWebView;
}


void tst_qtestcssperformance::cssPerfmGetMemoryUsed()
{

    QProcess *p = new QProcess;
    QString processName = "free";
    p->start(processName);
    QVERIFY(::waitForSignal(p, SIGNAL(finished(int))));
    QByteArray processOutput = p->readAll();
    QString res = processOutput;
    QStringList list = res.split(" ");
    list.removeAll("");

    QString qPath=":"+QString(s_tdkPath)+"/resources/translateY.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    } 

    m_view->setContent(line,"text/html");
    //m_view->show();

    QProcess *p1 = new QProcess;
    p1->start(processName);
    QVERIFY(::waitForSignal(p1, SIGNAL(finished(int))));
    QByteArray processOutput1 = p1->readAll();
    QString res1 = processOutput1;
    QStringList list1 = res1.split(" ");
    list1.removeAll("");

    qDebug() << "Totals: Memory used for css tranforms :: " << list1.at(7).toInt() - list.at(7).toInt() << "KB";
}

void tst_qtestcssperformance::cssPerfmGetMemoryForAnimation()
{
    QProcess *p = new QProcess;
    QString processName = "free";
    p->start(processName);
    QVERIFY(::waitForSignal(p, SIGNAL(finished(int))));
    QByteArray processOutput = p->readAll();
    QString res = processOutput;
    QStringList list = res.split(" ");
    list.removeAll("");

    QString qPath=":"+QString(s_tdkPath)+"/resources/keyframeAnimation.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QProcess *p1 = new QProcess;
    p1->start(processName);
    QVERIFY(::waitForSignal(p1, SIGNAL(finished(int))));
    QByteArray processOutput1 = p1->readAll();
    QString res1 = processOutput1;
    QStringList list1 = res1.split(" ");
    list1.removeAll("");

    qDebug() << "Totals : Memory used for css tranforms :: " << list1.at(7).toInt() - list.at(7).toInt() << "KB";

}

void tst_qtestcssperformance::cssPerfmMemoryUsedFor3dTransform()
{
    QProcess *p = new QProcess;
    QString processName = "free";
    p->start(processName);
    QVERIFY(::waitForSignal(p, SIGNAL(finished(int))));
    QByteArray processOutput = p->readAll();
    QString res = processOutput;
    QStringList list = res.split(" ");
    list.removeAll("");

    QString qPath=":"+QString(s_tdkPath)+"/resources/3dtransform.html";
    QFile file(qPath);

    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");
    //m_view->show();

    QProcess *p1 = new QProcess;
    p1->start(processName);
    QVERIFY(::waitForSignal(p1, SIGNAL(finished(int))));
    QByteArray processOutput1 = p1->readAll();
    QString res1 = processOutput1;
    QStringList list1 = res1.split(" ");
    list1.removeAll("");

    qDebug() << "Totals : Memory used for css tranforms :: " << list1.at(7).toInt() - list.at(7).toInt() << "KB";
}

void tst_qtestcssperformance::cssPerfmGetTimeToPlayAnimation()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/animation.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");


    pollingtimer = new QTimer(this);
    connect(pollingtimer, SIGNAL(timeout()), this, SLOT(slotAnimationStarted()));
    pollingtimer->start(1000);

    QVERIFY(::waitForSignal(pollingtimer,SIGNAL(destroyed())));

    qDebug() << "Totals : Time taken to play the animation ::" << videoLoadTime << "ms";
}


void tst_qtestcssperformance::slotAnimationStarted()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("isAnimationRunning()");
    if(result.toInt() == 0)
    {

        qDebug() << "Continue polling";

    }
    else
    {
       // qDebug()<< "Stop the timer";
        videoLoadTime = result.toInt();
        pollingtimer->stop();
        pollingtimer->deleteLater();
    }
}

void tst_qtestcssperformance::cssPerfmMemoryUsedForBackgroundChange()
{
    //m_view = new QWebView;
    QProcess *p = new QProcess;
    QString processName = "free";
    p->start(processName);
    QVERIFY(::waitForSignal(p, SIGNAL(finished(int))));
    QByteArray processOutput = p->readAll();
    QString res = processOutput;
    QStringList list = res.split(" ");
    list.removeAll("");

    QString qPath=":"+QString(s_tdkPath)+"/resources/hslColor.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");
    //m_view->show();

    QProcess *p1 = new QProcess;
    p1->start(processName);
    QVERIFY(::waitForSignal(p1, SIGNAL(finished(int))));
    QByteArray processOutput1 = p1->readAll();
    QString res1 = processOutput1;
    QStringList list1 = res1.split(" ");
    list1.removeAll("");

    qDebug() << "Totals : Memory used for background color change :: " << list1.at(7).toInt() - list.at(7).toInt() << "KB";
}

void tst_qtestcssperformance::cssPerfmTimeToLoadCSS2dTranforms()
{
    QString qPath="qrc:"+QString(s_tdkPath)+"/resources/translateY.html";
    QUrl url = QUrl(qPath);

    timer.start();
    //m_view->setContent(line,"text/html");
    m_view->load(url);

    connect(m_view,SIGNAL(loadFinished(bool)),this,SLOT(slotLoaded2dTransforms()));
    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));
}

void tst_qtestcssperformance::slotLoaded2dTransforms()
{
    qDebug() << "Totals : Time to load page with 2d transforms :: " << timer.elapsed() << "ms";
}

void tst_qtestcssperformance::cssPerfmTimeToLoadCSSTranforms()
{
    disconnect(m_view,SIGNAL(loadFinished(bool)),0,0);
    QString qPath="qrc:"+QString(s_tdkPath)+"/resources/3dtransform.html";
    QUrl url = QUrl(qPath);

    timer.start();
    //m_view->setContent(line,"text/html");
    m_view->load(url);

    connect(m_view,SIGNAL(loadFinished(bool)),this,SLOT(slotLoadedTransforms()));
    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));
}

void tst_qtestcssperformance::slotLoadedTransforms()
{
    qDebug() << "Totals : Time to load page with 3d transforms :: " << timer.elapsed() << "ms";
}

void tst_qtestcssperformance::cssPerfmTimeToFinishCSSAnimation()
{
   disconnect(m_view,SIGNAL(loadFinished(bool)),0,0);
   QString qPath="qrc:"+QString(s_tdkPath)+"/resources/keyframeAnimation.html";
   QUrl url = QUrl(qPath);

   timer.restart();
   m_view->load(url);

   pollingtimer = new QTimer(this);
   connect(pollingtimer, SIGNAL(timeout()), this, SLOT(slotFinishedAnimation()));
   pollingtimer->start(1000);

   QVERIFY(::waitForSignal(pollingtimer,SIGNAL(destroyed())));
}

void tst_qtestcssperformance::slotFinishedAnimation()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("isAnimationRunning()");
    if(result.toBool() == false)
    {

        qDebug() << "Continue polling";

    }
    else
    {
        qDebug() << "Totals : Time to finish the animation :: " << timer.elapsed() << "ms";
        pollingtimer->stop();
        pollingtimer->deleteLater();
    }
}

QTEST_MAIN(tst_qtestcssperformance)

#include "tst_qtestcssperformance.moc"

#include <QString>
#include <QtTest>
#include <QWebView>
#include <QWebFrame>
#include "../util.h"
char *s_tdkPath = getenv("TDK_PATH");
class tst_qtestcssfeatures_set3 : public QObject
{
    Q_OBJECT
    
public:
    tst_qtestcssfeatures_set3();
    
private Q_SLOTS:
    void init();
    void css3FuncRotateX();
    void css3FuncRotateY();
    void css3FuncRotateZ();
    void css3FuncTranslateX();
    void css3FuncTranslateY();
    void css3FuncTranslateZ();
    void css3FuncScaleX();
    void css3FuncScaleY();
    void css3FuncRotate3d();
    void css3Func3dTranslateZRotateZ();

private:
    QWebView* m_view;
};

tst_qtestcssfeatures_set3::tst_qtestcssfeatures_set3()
{
}

/*******************
 *To initialize the variables
 *needed to excute the test cases
 *****************/
void tst_qtestcssfeatures_set3::init()
{
    m_view = new QWebView;
}


void tst_qtestcssfeatures_set3::css3FuncRotateX()
{
    QWebView *m_view = new QWebView;

    QFile file(":/resources/rotateX.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("rotatedX()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(result.toInt(), 120);
}

void tst_qtestcssfeatures_set3::css3FuncRotateY()
{
    QWebView *m_view = new QWebView;

    QFile file(":/resources/rotateY.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("rotatedY()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(result.toInt(), 130);
}

void tst_qtestcssfeatures_set3::css3FuncRotateZ()
{
    QWebView *m_view = new QWebView;

    QFile file(":/resources/rotateZ.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("rotatedZ()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(result.toInt(), 30);
}

void tst_qtestcssfeatures_set3::css3FuncTranslateX()
{
    QWebView *m_view = new QWebView;

    QFile file(":/resources/translateX.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("translatedX()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(result.toInt(), 50);
}

void tst_qtestcssfeatures_set3::css3FuncTranslateY()
{
    QWebView *m_view = new QWebView;

    QFile file(":/resources/translateY.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("translatedY()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(result.toInt(), 80);
}

void tst_qtestcssfeatures_set3::css3FuncTranslateZ()
{
    QWebView *m_view = new QWebView;

    QFile file(":/resources/translateZ.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("translatedZ()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(result.toInt(), 80);
}

void tst_qtestcssfeatures_set3::css3FuncScaleX()
{
    QWebView *m_view = new QWebView;

    QFile file(":/resources/scaleX.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("ScaledX()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(result.toInt(), 2);
}

void tst_qtestcssfeatures_set3::css3FuncScaleY()
{
    QWebView *m_view = new QWebView;

    QFile file(":/resources/scaleY.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("ScaledY()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(result.toInt(), 4);
}

void tst_qtestcssfeatures_set3::css3FuncRotate3d()
{
    QWebView *m_view = new QWebView;

    QFile file(":/resources/rotate3d.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("Rotated3d()");
    qDebug() << "Getting the result "<< result.toString();

    QCOMPARE(result.toInt(), 60);

}

void tst_qtestcssfeatures_set3::css3Func3dTranslateZRotateZ()
{
    QWebView *m_view = new QWebView;

    QFile file(":/resources/rotatetranslate3d.html");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("RotatedTranslated3d()");
    qDebug() << "Getting the result "<< result.toString();
    QVERIFY2(result.toBool(),"Failure");

}

QTEST_MAIN(tst_qtestcssfeatures_set3)

#include "tst_qtestcssfeatures_set3.moc"

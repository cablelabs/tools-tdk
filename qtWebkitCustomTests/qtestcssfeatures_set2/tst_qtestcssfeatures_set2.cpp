#include <QString>
#include <QtTest>
#include <QWebView>
#include <QWebFrame>
#include "../util.h"
char *s_tdkPath = getenv("TDK_PATH");
class tst_qtestcssfeatures_set2 : public QObject
{
    Q_OBJECT
    
public:
    tst_qtestcssfeatures_set2();
    
private Q_SLOTS:
    void init();
    void css3FuncTranslateX();
    void css3FuncTranslateY();
    void css3FuncScaleX();
    void css3FuncScaleY();
    void css3FuncSkewX();
    void css3FuncSkewY();
    void css3FuncRotateX();
    void css3FuncMatrix();
    void css3FuncLoadCompundTransform();
    void css3FuncTranslateXY();
    void css3FuncScaleXY();
    void css3FuncSkewXY();

private:
    QWebView * m_view;
};

tst_qtestcssfeatures_set2::tst_qtestcssfeatures_set2()
{
}

void tst_qtestcssfeatures_set2::init()
{
    m_view = new QWebView;
}

void tst_qtestcssfeatures_set2::css3FuncTranslateX()
{

    m_view = new QWebView;
    QString qPath=":"+QString(s_tdkPath)+"/resources/translateX.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("isTranslated()");
    qDebug() << "Result obtained :: " << result.toString();
    QCOMPARE(result.toInt(),50);
}


void tst_qtestcssfeatures_set2::css3FuncTranslateY()
{
    m_view = new QWebView;
    QString qPath=":"+QString(s_tdkPath)+"/resources/translateY.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("isTranslated()");
    qDebug() << "Result obtained :: " << result.toString();
    QCOMPARE(result.toInt(),50);
}

void tst_qtestcssfeatures_set2::css3FuncScaleX()
{
    m_view = new QWebView;
    QString qPath=":"+QString(s_tdkPath)+"/resources/scaleX.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("isTranslated()");
    qDebug() << "Result obtained :: " << result.toString();
    QCOMPARE(result.toInt(),2);
}

void tst_qtestcssfeatures_set2::css3FuncScaleY()
{
    m_view = new QWebView;
    QString qPath=":"+QString(s_tdkPath)+"/resources/scaleY.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("isTranslated()");
    qDebug() << "Result obtained :: " << result.toString();
    QCOMPARE(result.toInt(),4);
}

void tst_qtestcssfeatures_set2::css3FuncSkewX()
{
    m_view = new QWebView;
    QString qPath=":"+QString(s_tdkPath)+"/resources/skewX.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("isTranslated()");
    qDebug() << "Result obtained :: " << result.toString();
    QCOMPARE(result.toInt(),30);
}

void tst_qtestcssfeatures_set2::css3FuncSkewY()
{
    m_view = new QWebView;
    QString qPath=":"+QString(s_tdkPath)+"/resources/skewY.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("isTranslated()");
    qDebug() << "Result obtained :: " << result.toString();
     QCOMPARE(result.toInt(),30);
}


void tst_qtestcssfeatures_set2::css3FuncRotateX()
{
    m_view = new QWebView;
    QString qPath=":"+QString(s_tdkPath)+"/resources/rotateX.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("isTranslated()");
    qDebug() << "Result obtained :: " << result.toString();
    QCOMPARE(result.toInt(),30);
}

void tst_qtestcssfeatures_set2::css3FuncMatrix()
{
    m_view = new QWebView;
    QString qPath=":"+QString(s_tdkPath)+"/resources/matrix.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("isTranslated()");
    qDebug() << "Result obtained :: " << result.toBool();
     QVERIFY(result.toBool());
}

void tst_qtestcssfeatures_set2::css3FuncLoadCompundTransform()
{
    m_view = new QWebView;
    QString qPath=":"+QString(s_tdkPath)+"/resources/compoundTransform.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("isTranslated()");
    qDebug() << "Result obtained :: " << result.toBool();
    QVERIFY(result.toBool());
}

void tst_qtestcssfeatures_set2::css3FuncTranslateXY()
{
    m_view = new QWebView;
    QString qPath=":"+QString(s_tdkPath)+"/resources/translateXY.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("isTranslated()");
    qDebug() << "Result obtained :: " << result.toBool();
    QVERIFY(result.toBool());
}

void tst_qtestcssfeatures_set2::css3FuncScaleXY()
{
    m_view = new QWebView;
    QString qPath=":"+QString(s_tdkPath)+"/resources/scaleXY.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("isTranslated()");
    qDebug() << "Result obtained :: " << result.toBool();
    QVERIFY(result.toBool());
}

void tst_qtestcssfeatures_set2::css3FuncSkewXY()
{
    m_view = new QWebView;
    QString qPath=":"+QString(s_tdkPath)+"/resources/skewXY.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("isTranslated()");
    qDebug() << "Result obtained :: " << result.toBool();
    QVERIFY(result.toBool());
}

QTEST_MAIN(tst_qtestcssfeatures_set2)

#include "tst_qtestcssfeatures_set2.moc"

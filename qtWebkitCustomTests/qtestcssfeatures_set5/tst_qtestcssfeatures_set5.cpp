#include <QString>
#include <QtTest>
#include <QWebView>
#include <QWebFrame>
char *s_tdkPath = getenv("TDK_PATH");
class tst_qtestcssfeatures_set5 : public QObject
{
    Q_OBJECT
    
public:
    tst_qtestcssfeatures_set5();
    
private Q_SLOTS:
    void cssFunctLetterSpacing();
    void cssFunctOverflowX();
    void cssFunctDirection();
    void cssFunctBorderStyle();
    void cssFunctBorderColor();
    void cssFunctOrder();
    void cssFunctFirstChild();
    void cssFunctCaption();
    void cssFunctListStyle();
    void cssFunctLineHeight();
    void cssFunctOutlineColor();
    void cssFunctOverflowY();
    void cssFunctResize();
    void cssFunctScale();
    void cssFunctTableLayout();


private:
    QWebView* m_view;
};


tst_qtestcssfeatures_set5::tst_qtestcssfeatures_set5()
{
}

/*******************
 * Loads a web page with
 * CSS empty cells element
 *****************/

void tst_qtestcssfeatures_set5::cssFunctLetterSpacing()
{
    m_view = new QWebView;

    QString qPath=":"+QString(s_tdkPath)+"/resources/cssLetterSpacing.html";
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

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifyLetterSpacing()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(QString(result.toString()),QString("2px"));
}

void tst_qtestcssfeatures_set5::cssFunctOverflowX()
{
    m_view = new QWebView;

    QString qPath=":"+QString(s_tdkPath)+"/resources/cssOverflowX.html";
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

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifyOverflowX()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(QString(result.toString()),QString("hidden"));
}

void tst_qtestcssfeatures_set5::cssFunctDirection()
{
    m_view = new QWebView;

    QString qPath=":"+QString(s_tdkPath)+"/resources/cssDirection.html";
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

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifyDirection()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(QString(result.toString()),QString("rtl"));
}

void tst_qtestcssfeatures_set5::cssFunctBorderStyle()
{
    m_view = new QWebView;

    QString qPath=":"+QString(s_tdkPath)+"/resources/cssBorderStyle.html";
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

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifyBorderStyle()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(QString(result.toString()),QString("dotted"));
}

void tst_qtestcssfeatures_set5::cssFunctBorderColor()
{
    m_view = new QWebView;

    QString qPath=":"+QString(s_tdkPath)+"/resources/cssBorderColor.html";
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

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifyBorderColor()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(QString(result.toString()),QString("rgb(255, 0, 0) rgb(0, 255, 0) rgb(0, 0, 255) rgb(250, 0, 255)"));
}

void tst_qtestcssfeatures_set5::cssFunctOrder()
{
    m_view = new QWebView;

    QString qPath=":"+QString(s_tdkPath)+"/resources/cssOrder.html";
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

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifyOrder()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(QString(result.toString()),QString("2"));
}

void tst_qtestcssfeatures_set5::cssFunctFirstChild()
{
    m_view = new QWebView;

    QString qPath=":"+QString(s_tdkPath)+"/resources/cssFirstChild.html";
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

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifyFirstChild()");
    qDebug() << "Getting the result "<< result.toString();
    QVERIFY(result.toBool());
}

void tst_qtestcssfeatures_set5::cssFunctCaption()
{
    m_view = new QWebView;

    QString qPath=":"+QString(s_tdkPath)+"/resources/cssCaption.html";
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

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifyCaption()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(QString(result.toString()),QString("bottom"));
}

void tst_qtestcssfeatures_set5::cssFunctListStyle()
{
    m_view = new QWebView;

    QString qPath=":"+QString(s_tdkPath)+"/resources/cssListStyle.html";
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

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifyListStyle()");
    qDebug() << "Getting the result "<< result.toString();
    QVERIFY(result.toBool());
}

void tst_qtestcssfeatures_set5::cssFunctLineHeight()
{
    m_view = new QWebView;

    QString qPath=":"+QString(s_tdkPath)+"/resources/cssLineHeight.html";
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

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifyLineHeight()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(QString(result.toString()),QString("3"));
}

void tst_qtestcssfeatures_set5::cssFunctOutlineColor()
{
    m_view = new QWebView;

    QString qPath=":"+QString(s_tdkPath)+"/resources/cssOutlineColor.html";
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

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifyOutlineColor()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(QString(result.toString()),QString("rgb(0, 255, 0)"));
}

void tst_qtestcssfeatures_set5::cssFunctOverflowY()
{
    m_view = new QWebView;

    QString qPath=":"+QString(s_tdkPath)+"/resources/cssOverflowY.html";
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

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifyOverflowY()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(QString(result.toString()),QString("hidden"));
}

void tst_qtestcssfeatures_set5::cssFunctResize()
{
    m_view = new QWebView;

    QString qPath=":"+QString(s_tdkPath)+"/resources/cssResize.html";
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

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifyResize()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(QString(result.toString()),QString("both"));
}

void tst_qtestcssfeatures_set5::cssFunctScale()
{
    m_view = new QWebView;

    QString qPath=":"+QString(s_tdkPath)+"/resources/cssScale.html";
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

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifyScale()");
    qDebug() << "Getting the result "<< result.toString();
    QVERIFY(result.toBool());
}

void tst_qtestcssfeatures_set5::cssFunctTableLayout()
{
    m_view = new QWebView;

    QString qPath=":"+QString(s_tdkPath)+"/resources/cssTableLayout.html";
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

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifyTableLayout()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(QString(result.toString()),QString("fixed"));
}
QTEST_MAIN(tst_qtestcssfeatures_set5)

#include "tst_qtestcssfeatures_set5.moc"

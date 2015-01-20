#include <QString>
#include <QtTest>
#include <QWebView>
#include <QWebFrame>
char *s_tdkPath = getenv("TDK_PATH");
class tst_qtestcssgenericfeatures : public QObject
{
    Q_OBJECT
    
public:
    tst_qtestcssgenericfeatures();
    
private Q_SLOTS:
    void cssFunctBackgroundAttachment();
    void cssFunctTextColor();
    void cssFunctTextAlignment();
    void cssFunctTextDecoration();
    void cssFunctTextTransform();
    void cssFunctTextIndentation();

    void cssFunctOutline();

    void cssFunctTextLeftPadding();
    void cssFunctTextRightPadding();
    void cssFunctTextTopPadding();
    void cssFunctTextBottomPadding();

    void cssFunctTextLeftMargin();
    void cssFunctTextRightMargin();
    void cssFunctTextTopMargin();
    void cssFunctTextBottomMargin();

    void cssFunctLeftBorderWidth();
    void cssFunctLeftBorderColor();
    void cssFunctLeftBorderStyle();


    void cssFunctRightBorderColor();
    void cssFunctRightBorderWidth();
    void cssFunctRightBorderStyle();


    void cssFunctTopBorderWidth();
    void cssFunctTopBorderColor();
    void cssFunctTopBorderStyle();

    void cssFunctBottomBorderColor();
    void cssFunctBottomBorderStyle();
    void cssFunctBottomBorderWidth();


    void cssFunctLeftBorder();
    void cssFunctRightBorder();
    void cssFunctTopBorder();
    void cssFunctBottomBorder();
private:
    QWebView * m_view;
};

tst_qtestcssgenericfeatures::tst_qtestcssgenericfeatures()
{
        m_view = new QWebView;
}

void tst_qtestcssgenericfeatures::cssFunctBackgroundAttachment()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/backgroundImage.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("isBackgroundAttached()");
    qDebug() << "Result obtained :: " << result.toString();
    QVERIFY(result.toBool());
}

void tst_qtestcssgenericfeatures::cssFunctTextColor()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/textstyle.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("textColor()");
    qDebug() << "Result obtained :: " << result.toString();
    QVERIFY(result.toBool());
}

void tst_qtestcssgenericfeatures::cssFunctTextAlignment()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/textstyle.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("textAlignment()");
    qDebug() << "Result obtained :: " << result.toString();
    QVERIFY(result.toBool());
}


void tst_qtestcssgenericfeatures::cssFunctTextDecoration()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/textstyle.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("textDecoration()");
    qDebug() << "Result obtained :: " << result.toString();
    QVERIFY(result.toBool());
}


void tst_qtestcssgenericfeatures::cssFunctTextTransform()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/textstyle.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("textTransformation()");
    qDebug() << "Result obtained :: " << result.toString();
    QVERIFY(result.toBool());
}

void tst_qtestcssgenericfeatures::cssFunctTextIndentation()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/textstyle.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("textIndentation()");
    qDebug() << "Result obtained :: " << result.toString();
    QVERIFY(result.toBool());
}

void tst_qtestcssgenericfeatures::cssFunctOutline()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/cssoutline.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("setDottedOutline()");
    qDebug() << "Result obtained :: " << result.toString();
    QVERIFY(result.toBool());
}

void tst_qtestcssgenericfeatures::cssFunctTextLeftPadding()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/textpadding.html";
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


    QVariant resultLeft = m_view->page()->mainFrame()->evaluateJavaScript("leftPadding()");
    qDebug() << "Result obtained :: " << resultLeft.toString();
    QCOMPARE(resultLeft.toString(),QString("50px"));
}

void tst_qtestcssgenericfeatures::cssFunctTextRightPadding()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/textpadding.html";
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


    QVariant resultRight = m_view->page()->mainFrame()->evaluateJavaScript("rightPadding()");
    qDebug() << "Result obtained :: " << resultRight.toString();
    QCOMPARE(resultRight.toString(),QString("50px"));
}

void tst_qtestcssgenericfeatures::cssFunctTextTopPadding()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/textpadding.html";
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


    QVariant resultTop = m_view->page()->mainFrame()->evaluateJavaScript("topPadding()");
    qDebug() << "Result obtained :: " << resultTop.toString();
    QCOMPARE(resultTop.toString(),QString("25px"));
}

void tst_qtestcssgenericfeatures::cssFunctTextBottomPadding()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/textpadding.html";
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


    QVariant resultBottom = m_view->page()->mainFrame()->evaluateJavaScript("bottomPadding()");
    qDebug() << "Result obtained :: " << resultBottom.toString();
    QCOMPARE(resultBottom.toString(),QString("25px"));
}


void tst_qtestcssgenericfeatures::cssFunctTextLeftMargin()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/textpadding.html";
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


    QVariant resultLeft = m_view->page()->mainFrame()->evaluateJavaScript("leftMargin()");
    qDebug() << "Result obtained :: " << resultLeft.toString();
    QCOMPARE(resultLeft.toString(),QString("50px"));
}

void tst_qtestcssgenericfeatures::cssFunctTextRightMargin()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/textpadding.html";
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

    QVariant resultRight = m_view->page()->mainFrame()->evaluateJavaScript("rightMargin()");
    qDebug() << "Result obtained :: " << resultRight.toString();
    QCOMPARE(resultRight.toString(),QString("50px"));

}

void tst_qtestcssgenericfeatures::cssFunctTextTopMargin()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/textpadding.html";
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

    QVariant resultTop = m_view->page()->mainFrame()->evaluateJavaScript("topMargin()");
    qDebug() << "Result obtained :: " << resultTop.toString();
    QCOMPARE(resultTop.toString(),QString("100px"));
}

void tst_qtestcssgenericfeatures::cssFunctTextBottomMargin()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/textpadding.html";
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

    QVariant resultBottom = m_view->page()->mainFrame()->evaluateJavaScript("bottomMargin()");
    qDebug() << "Result obtained :: " << resultBottom.toString();
    QCOMPARE(resultBottom.toString(),QString("100px"));
}

void tst_qtestcssgenericfeatures::cssFunctLeftBorder()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/textborder.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("leftBorder()");
    qDebug() << "Result obtained :: " << result.toString();
    QVERIFY(result.toBool());
}


void tst_qtestcssgenericfeatures::cssFunctLeftBorderColor()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/textborder.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("leftBorderColor()");
    qDebug() << "Result obtained :: " << result.toString();
    QCOMPARE(result.toString(),QString("rgb(255, 0, 0)"));
}

void tst_qtestcssgenericfeatures::cssFunctLeftBorderStyle()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/textborder.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("leftBorderStyle()");
    qDebug() << "Result obtained :: " << result.toString();
    QCOMPARE(result.toString(),QString("solid"));
}

void tst_qtestcssgenericfeatures::cssFunctLeftBorderWidth()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/textborder.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("leftBorderWidth()");
    qDebug() << "Result obtained :: " << result.toString();
    QCOMPARE(result.toString(),QString("2px"));
}

void tst_qtestcssgenericfeatures::cssFunctRightBorder()
{

    QString qPath=":"+QString(s_tdkPath)+"/resources/textborder.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("rightBorder()");
    qDebug() << "Result obtained :: " << result.toString();
    QVERIFY(result.toBool());
}

void tst_qtestcssgenericfeatures::cssFunctRightBorderColor()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/textborder.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("rightBorderColor()");
    qDebug() << "Result obtained :: " << result.toString();
    QCOMPARE(result.toString(),QString("rgb(0, 128, 0)"));
}

void tst_qtestcssgenericfeatures::cssFunctRightBorderStyle()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/textborder.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("rightBorderStyle()");
    qDebug() << "Result obtained :: " << result.toString();
    QCOMPARE(result.toString(),QString("dotted"));
}

void tst_qtestcssgenericfeatures::cssFunctRightBorderWidth()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/textborder.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("rightBorderWidth()");
    qDebug() << "Result obtained :: " << result.toString();
    QCOMPARE(result.toString(),QString("2px"));
}

void tst_qtestcssgenericfeatures::cssFunctTopBorder()
{

    QString qPath=":"+QString(s_tdkPath)+"/resources/textborder.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("topBorder()");
    qDebug() << "Result obtained :: " << result.toString();
    QVERIFY(result.toBool());
}


void tst_qtestcssgenericfeatures::cssFunctTopBorderColor()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/textborder.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("topBorderColor()");
    qDebug() << "Result obtained :: " << result.toString();
    QCOMPARE(result.toString(),QString("rgb(0, 0, 255)"));
}

void tst_qtestcssgenericfeatures::cssFunctTopBorderStyle()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/textborder.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("topBorderStyle()");
    qDebug() << "Result obtained :: " << result.toString();
    QCOMPARE(result.toString(),QString("dashed"));
}

void tst_qtestcssgenericfeatures::cssFunctTopBorderWidth()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/textborder.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("topBorderWidth()");
    qDebug() << "Result obtained :: " << result.toString();
    QCOMPARE(result.toString(),QString("2px"));
}

void tst_qtestcssgenericfeatures::cssFunctBottomBorder()
{

    QString qPath=":"+QString(s_tdkPath)+"/resources/textborder.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("bottomBorder()");
    qDebug() << "Result obtained :: " << result.toString();
    QVERIFY(result.toBool());
}



void tst_qtestcssgenericfeatures::cssFunctBottomBorderColor()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/textborder.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("bottomBorderColor()");
    qDebug() << "Result obtained :: " << result.toString();
    QCOMPARE(result.toString(),QString("rgb(255, 0, 0)"));
}

void tst_qtestcssgenericfeatures::cssFunctBottomBorderStyle()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/textborder.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("bottomBorderStyle()");
    qDebug() << "Result obtained :: " << result.toString();
    QCOMPARE(result.toString(),QString("double"));
}

void tst_qtestcssgenericfeatures::cssFunctBottomBorderWidth()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/textborder.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("bottomBorderWidth()");
    qDebug() << "Result obtained :: " << result.toString();
    QCOMPARE(result.toString(),QString("2px"));
}
QTEST_MAIN(tst_qtestcssgenericfeatures)

#include "tst_qtestcssgenericfeatures.moc"

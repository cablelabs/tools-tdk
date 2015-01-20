#include <QString>
#include <QtTest>
#include <QWebView>
#include <QWebFrame>
char *s_tdkPath = getenv("TDK_PATH");
class tst_qtestcssselectors : public QObject
{
    Q_OBJECT
    
public:
    tst_qtestcssselectors();
    
private Q_SLOTS:
    void css3FuncClassSelectors();
    void css3FuncIdSelectors();
    void css3FuncAllSelector();
    void css3FuncElementSelector();
    void css3FuncMultipleElementSelector();
    void css3FuncNestedSelector();
    void css3FuncChildElementSelector();
    void css3FuncSiblingSelector();

    //Attribute Selectors
    void css3FuncTargetAttributeSelector();
    void css3FuncTargetBlankSelector();
    void css3FuncTitleAttributeSelector();
    void css3FuncLangAttributeSelector();

    void css3FuncPrecedingElementSelector();
    void css3FuncAttributeByPrefixSelector();
    void css3FuncAttributeEndsWithSelector();
    void css3FuncAttributeContainsSelector();
    void css3FuncNotSelector();
    void css3FuncInputDisabledSelector();
    void css3FuncInputEnabledSelector();
    void css3FuncEmptySelector();
    void css3FuncRootSelector();
    void css3FuncFirstOfTypeSelector();

    //Not yet Committed
    void css3FuncLastOfTypeSelector();
    void css3FuncOnlyChildSelector();
    void css3FuncOnlyOfTypeSelector();
    void css3FuncLastChildSelector();

    void css3FuncNthChildSelector();
    void css3FuncNthLastChildSelector();
    void css3FuncNthOfTypeSelector();
    void css3FuncNthlastOfTypeSelector();

private:
    QWebView * m_view;
};

tst_qtestcssselectors::tst_qtestcssselectors()
{
    m_view = new QWebView;
}

/**
 * @brief tst_qtestcssselectors::testClassSelectors
 */
void tst_qtestcssselectors::css3FuncClassSelectors()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/classselectors.html";
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


void tst_qtestcssselectors::css3FuncIdSelectors()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/idselectors.html";
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

void tst_qtestcssselectors::css3FuncAllSelector()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/allselectors.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("backgroundColor()");
    qDebug() << "Result obtained :: " << result.toString();
    QVERIFY(result.toBool());
}

void tst_qtestcssselectors::css3FuncElementSelector()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/elementselector.html";
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

void tst_qtestcssselectors::css3FuncMultipleElementSelector()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/mulitpleelementselector.html";
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

void tst_qtestcssselectors::css3FuncNestedSelector()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/nestedselector.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("textBackground()");
    qDebug() << "Result obtained :: " << result.toString();
    QCOMPARE(result.toString(),QString("rgb(255, 255, 0)"));
}

void tst_qtestcssselectors::css3FuncChildElementSelector()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/childselector.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("textBackground()");
    qDebug() << "Result obtained :: " << result.toString();
    QCOMPARE(result.toString(),QString("rgb(255, 255, 0)"));
}

void tst_qtestcssselectors::css3FuncSiblingSelector()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/siblingselector.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("textBackground()");
    qDebug() << "Result obtained :: " << result.toString();
    QCOMPARE(result.toString(),QString("rgb(255, 255, 0)"));
}

void tst_qtestcssselectors::css3FuncTargetAttributeSelector()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/targetselector.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("textBackground()");
    qDebug() << "Result obtained :: " << result.toString();
    QCOMPARE(result.toString(),QString("rgb(255, 255, 0)"));
}

void tst_qtestcssselectors::css3FuncTargetBlankSelector()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/targetblankselector.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("textBackground()");
    qDebug() << "Result obtained :: " << result.toString();
    QCOMPARE(result.toString(),QString("rgb(255, 255, 0)"));
}

void tst_qtestcssselectors::css3FuncTitleAttributeSelector()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/titleattributeselector.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("textBackground()");
    qDebug() << "Result obtained :: " << result.toString();
    QCOMPARE(result.toString(),QString("rgb(255, 255, 0)"));
}

void tst_qtestcssselectors::css3FuncLangAttributeSelector()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/langattributeselector.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("textBackground()");
    qDebug() << "Result obtained :: " << result.toString();
    QCOMPARE(result.toString(),QString("rgb(255, 255, 0)"));
}

void tst_qtestcssselectors::css3FuncPrecedingElementSelector()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/precedingelementselector.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("textBackground()");
    qDebug() << "Result obtained :: " << result.toString();
    QVERIFY(result.toBool());
}

void tst_qtestcssselectors::css3FuncAttributeByPrefixSelector()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/attributeprefixselector.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("textBackground()");
    qDebug() << "Result obtained :: " << result.toString();
    QVERIFY(result.toBool());
}

void tst_qtestcssselectors::css3FuncAttributeEndsWithSelector()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/attributeprefixselector.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("endsWithSelector()");
    qDebug() << "Result obtained :: " << result.toString();
    QVERIFY(result.toBool());
}

void tst_qtestcssselectors::css3FuncAttributeContainsSelector()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/attributecontainsselector.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("textBackground()");
    qDebug() << "Result obtained :: " << result.toString();
    QVERIFY(result.toBool());
}

void tst_qtestcssselectors::css3FuncNotSelector()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/notselector.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("color()");
    qDebug() << "Result obtained :: " << result.toString();
    QVERIFY(result.toBool());
}

void tst_qtestcssselectors::css3FuncInputDisabledSelector()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/inputdisabledselector.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("getBackground()");
    qDebug() << "Result obtained :: " << result.toString();
    QVERIFY(result.toBool());
}

void tst_qtestcssselectors::css3FuncInputEnabledSelector()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/inputdisabledselector.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("getEnabledBackground()");
    qDebug() << "Result obtained :: " << result.toString();
    QVERIFY(result.toBool());
}

void tst_qtestcssselectors::css3FuncEmptySelector()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/emptyselector.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("getBackground()");
    qDebug() << "Result obtained :: " << result.toString();
    QVERIFY(result.toBool());
}

void tst_qtestcssselectors::css3FuncRootSelector()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/rootselector.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("getBackground()");
    qDebug() << "Result obtained :: " << result.toString();
    QCOMPARE(result.toString(),QString("rgb(255, 0, 0)"));
}

void tst_qtestcssselectors::css3FuncFirstOfTypeSelector()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/firstoftypeselector.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("getBackground()");
    qDebug() << "Result obtained :: " << result.toString();
     QVERIFY(result.toBool());
}

void tst_qtestcssselectors::css3FuncLastOfTypeSelector()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/lastoftypeselector.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("getBackground()");
    qDebug() << "Result obtained :: " << result.toString();
    QVERIFY(result.toBool());
}

void tst_qtestcssselectors::css3FuncOnlyChildSelector()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/onlychildselector.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("getBackground()");
    qDebug() << "Result obtained :: " << result.toString();
    QVERIFY(result.toBool());
}

void tst_qtestcssselectors::css3FuncOnlyOfTypeSelector()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/onlyoftypeselector.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("getBackground()");
    qDebug() << "Result obtained :: " << result.toString();
    QVERIFY(result.toBool());
}

void tst_qtestcssselectors::css3FuncLastChildSelector()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/lastchildselector.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("getBackground()");
    qDebug() << "Result obtained :: " << result.toString();
    QVERIFY(result.toBool());
}

void tst_qtestcssselectors::css3FuncNthChildSelector()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/nthchildselector.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("getBackground()");
    qDebug() << "Result obtained :: " << result.toString();
    QVERIFY(result.toBool());
}

void tst_qtestcssselectors::css3FuncNthLastChildSelector()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/nthlastchildselector.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("getBackground()");
    qDebug() << "Result obtained :: " << result.toString();
    QVERIFY(result.toBool());
}

void tst_qtestcssselectors::css3FuncNthOfTypeSelector()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/nthoftypeselector.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("getBackground()");
    qDebug() << "Result obtained :: " << result.toString();
    QVERIFY(result.toBool());
}

void tst_qtestcssselectors::css3FuncNthlastOfTypeSelector()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/nthlastoftypeselector.html";
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


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("getBackground()");
    qDebug() << "Result obtained :: " << result.toString();
    QVERIFY(result.toBool());
}


QTEST_MAIN(tst_qtestcssselectors)
#include "tst_qtestcssselectors.moc"

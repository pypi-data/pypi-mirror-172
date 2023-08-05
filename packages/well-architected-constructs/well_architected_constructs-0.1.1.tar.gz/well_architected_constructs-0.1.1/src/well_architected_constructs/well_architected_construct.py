import aws_cdk
import constructs


class WellArchitected(constructs.Construct):

    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        error_topic=None,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)
        self.error_topic = error_topic

    def create_sns_topic(self, display_name):
        return aws_cdk.aws_sns.Topic(
            self, display_name,
            display_name=display_name,
        )

    @staticmethod
    def create_cloudwatch_math_expression(expression=None, label=None, using_metrics=None):
        return aws_cdk.aws_cloudwatch.MathExpression(
            expression=expression,
            label=label,
            using_metrics=using_metrics,
            period=aws_cdk.Duration.minutes(5),
        )

    def cloudwatch_math_sum(self, label=None, m1=None, m2=None):
        return self.create_cloudwatch_math_expression(
            label=label,
            expression="m1 + m2",
            using_metrics={"m1": m1, "m2": m2},
        )

    @staticmethod
    def create_cloudwatch_widget(title=None, stacked=True, left=None):
        return aws_cdk.aws_cloudwatch.GraphWidget(
            title=title, width=8, stacked=stacked, left=left
        )

    def create_cloudwatch_alarm(self, id=None, metric=None, threshold=1):
        alarm = aws_cdk.aws_cloudwatch.Alarm(
            self,
            id=id,
            metric=metric,
            threshold=threshold,
            evaluation_periods=6,
            datapoints_to_alarm=1,
            treat_missing_data=aws_cdk.aws_cloudwatch.TreatMissingData.NOT_BREACHING,
        )
        if self.error_topic:
            alarm.add_alarm_action(
                aws_cdk.aws_cloudwatch_actions.SnsAction(self.error_topic)
            )

    def create_cloudwatch_widgets(self):
        raise NotImplementedError
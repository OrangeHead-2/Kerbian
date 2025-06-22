#import "ErrorReporter.h"

static id _eventSink = nil;

@implementation ErrorReporter
+ (void)setEventSink:(id)sink { _eventSink = sink; }
+ (void)report:(NSString *)errorType message:(NSString *)message details:(NSDictionary *)details {
    if (_eventSink && [_eventSink respondsToSelector:@selector(send:)]) {
        NSDictionary *err = @{
            @"type": @"error",
            @"error_type": errorType,
            @"message": message,
            @"details": details ?: @{}
        };
        NSData *jsonData = [NSJSONSerialization dataWithJSONObject:err options:0 error:nil];
        NSString *jsonLine = [[NSString alloc] initWithData:jsonData encoding:NSUTF8StringEncoding];
        [_eventSink send:jsonLine];
    }
}
@end
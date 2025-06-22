#import "BridgeEventRouter.h"
#import "ErrorReporter.h"

static id _eventSink = nil;

@implementation BridgeEventRouter
+ (void)setEventSink:(id)sink { _eventSink = sink; }
+ (void)emit:(NSString *)event viewId:(NSInteger)viewId data:(NSDictionary *)data {
    @try {
        if (_eventSink && [_eventSink respondsToSelector:@selector(send:)]) {
            NSDictionary *msg = @{
                @"type": @"event",
                @"event": event,
                @"view_id": @(viewId),
                @"data": data ?: @{}
            };
            NSData *jsonData = [NSJSONSerialization dataWithJSONObject:msg options:0 error:nil];
            NSString *jsonLine = [[NSString alloc] initWithData:jsonData encoding:NSUTF8StringEncoding];
            [_eventSink send:jsonLine];
        }
    }
    @catch (NSException *e) {
        [ErrorReporter report:@"BridgeError" message:[NSString stringWithFormat:@"Failed to emit event: %@", event] details:@{@"exception": e.reason ?: @""}];
    }
}
@end
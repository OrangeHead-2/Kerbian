#import "KerbianBridge.h"
#import "UIManager.h"

@implementation KerbianBridge {
    NSFileHandle *_readHandle;
    NSFileHandle *_writeHandle;
    UIManager *_uiManager;
}

- (instancetype)initWithPort:(int)port {
    self = [super init];
    if (self) {
        // Create socket server at port, accept connection
        // Assign _readHandle and _writeHandle
        _uiManager = [[UIManager alloc] init];
    }
    return self;
}

- (void)start {
    dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
        while (true) {
            NSData *data = [_readHandle availableData];
            if (data.length == 0) break;
            NSString *line = [[NSString alloc] initWithData:data encoding:NSUTF8StringEncoding];
            [self handleMessage:line];
        }
    });
}

- (void)handleMessage:(NSString *)line {
    NSData *jsonData = [line dataUsingEncoding:NSUTF8StringEncoding];
    NSDictionary *msg = [NSJSONSerialization JSONObjectWithData:jsonData options:0 error:nil];
    NSString *type = msg[@"type"];
    if ([type isEqualToString:@"call"] && [msg[@"target"] isEqualToString:@"UIManager"]) {
        NSString *method = msg[@"method"];
        NSDictionary *args = msg[@"args"];
        if ([method isEqualToString:@"create_view"]) {
            NSInteger viewId = [_uiManager createView:args[@"type"] props:args[@"props"]];
            NSDictionary *resp = @{
                @"type": @"response",
                @"id": msg[@"id"],
                @"result": @{@"view_id": @(viewId)}
            };
            NSData *respData = [NSJSONSerialization dataWithJSONObject:resp options:0 error:nil];
            [_writeHandle writeData:respData];
            [_writeHandle writeData:[@"\n" dataUsingEncoding:NSUTF8StringEncoding]];
        }
        // ... handle other methods
    }
    // ... handle other targets and message types
}

@end
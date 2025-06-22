#import <Foundation/Foundation.h>

@interface BridgeEventRouter : NSObject
+ (void)setEventSink:(id)sink;
+ (void)emit:(NSString *)event viewId:(NSInteger)viewId data:(NSDictionary *)data;
@end
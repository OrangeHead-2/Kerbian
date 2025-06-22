#import <Foundation/Foundation.h>

@interface ErrorReporter : NSObject
+ (void)setEventSink:(id)sink;
+ (void)report:(NSString *)errorType message:(NSString *)message details:(NSDictionary *)details;
@end
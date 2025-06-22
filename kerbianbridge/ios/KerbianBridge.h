#import <Foundation/Foundation.h>

@interface KerbianBridge : NSObject
- (instancetype)initWithPort:(int)port;
- (void)start;
@end
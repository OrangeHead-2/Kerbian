#import "UIManager.h"
#import "BridgeEventRouter.h"
#import "ErrorReporter.h"
#import <UIKit/UIKit.h>

@implementation UIManager {
    NSMutableDictionary *_views;
    NSInteger _nextId;
    UIView *_rootView;
}

- (instancetype)initWithRootView:(UIView *)rootView {
    self = [super init];
    if (self) {
        _views = [NSMutableDictionary new];
        _nextId = 1;
        _rootView = rootView;
    }
    return self;
}

- (NSInteger)createView:(NSString *)type props:(NSDictionary *)props {
    @try {
        UIView *v = nil;
        NSInteger vid = _nextId++;
        if ([type isEqualToString:@"Button"]) {
            UIButton *button = [UIButton buttonWithType:UIButtonTypeSystem];
            [button setTitle:props[@"text"] forState:UIControlStateNormal];
            button.tag = vid;
            [button addTarget:self action:@selector(buttonPressed:) forControlEvents:UIControlEventTouchUpInside];
            v = button;
        } else if ([type isEqualToString:@"Text"]) {
            UILabel *label = [[UILabel alloc] init];
            label.text = props[@"value"];
            label.tag = vid;
            v = label;
        } else if ([type isEqualToString:@"Image"]) {
            UIImageView *imageView = [[UIImageView alloc] init];
            NSString *src = props[@"src"];
            if (src) imageView.image = [UIImage imageWithContentsOfFile:src];
            imageView.tag = vid;
            v = imageView;
        } else if ([type isEqualToString:@"List"]) {
            UITableView *table = [[UITableView alloc] init];
            table.tag = vid;
            // DataSource/Delegate to be assigned by integration layer
            v = table;
        } else if ([type isEqualToString:@"Modal"]) {
            NSString *message = props[@"message"] ?: @"";
            UIAlertController *alert = [UIAlertController alertControllerWithTitle:nil message:message preferredStyle:UIAlertControllerStyleAlert];
            [alert addAction:[UIAlertAction actionWithTitle:@"OK" style:UIAlertActionStyleDefault handler:^(UIAlertAction *action) {
                [BridgeEventRouter emit:@"onModalClose" viewId:-1 data:nil];
            }]];
            UIViewController *root = UIApplication.sharedApplication.keyWindow.rootViewController;
            [root presentViewController:alert animated:YES completion:nil];
            return -1;
        } else {
            [ErrorReporter report:@"UIError" message:[NSString stringWithFormat:@"Unknown view type: %@", type] details:@{}];
            return -1;
        }
        if (v) {
            [_rootView addSubview:v];
            _views[@(vid)] = v;
            return vid;
        }
    }
    @catch (NSException *e) {
        [ErrorReporter report:@"UIError" message:[NSString stringWithFormat:@"Failed to create view: %@", type] details:@{@"exception": e.reason ?: @""}];
    }
    return -1;
}

- (void)updateView:(NSInteger)vid props:(NSDictionary *)props {
    @try {
        UIView *v = _views[@(vid)];
        if ([v isKindOfClass:[UILabel class]] && props[@"value"]) {
            ((UILabel *)v).text = props[@"value"];
        } else if ([v isKindOfClass:[UIButton class]] && props[@"text"]) {
            [((UIButton *)v) setTitle:props[@"text"] forState:UIControlStateNormal];
        } else if ([v isKindOfClass:[UIImageView class]] && props[@"src"]) {
            ((UIImageView *)v).image = [UIImage imageWithContentsOfFile:props[@"src"]];
        }
    }
    @catch (NSException *e) {
        [ErrorReporter report:@"UIError" message:[NSString stringWithFormat:@"Failed to update view: %ld", (long)vid] details:@{@"exception": e.reason ?: @""}];
    }
}

- (void)removeView:(NSInteger)vid {
    @try {
        UIView *v = _views[@(vid)];
        [v removeFromSuperview];
        [_views removeObjectForKey:@(vid)];
    }
    @catch (NSException *e) {
        [ErrorReporter report:@"UIError" message:[NSString stringWithFormat:@"Failed to remove view: %ld", (long)vid] details:@{@"exception": e.reason ?: @""}];
    }
}

- (void)buttonPressed:(UIButton *)sender {
    [BridgeEventRouter emit:@"onPress" viewId:sender.tag data:nil];
}
@end
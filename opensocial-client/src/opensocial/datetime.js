import * as dayjs from 'dayjs'
import * as relativeTime from 'dayjs/plugin/relativeTime'
dayjs().format()
dayjs.extend(relativeTime)


class OpenSocialDate {
    timeFromNow(utc) {
        return dayjs().from(dayjs(utc))
    }
}

export default OpenSocialDate